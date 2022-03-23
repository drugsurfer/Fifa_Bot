from threading import Thread
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Strategy import StrategyFromEndSell


class Sell:
    def __init__(self, parent):
        self.parent = parent
        self.count_bought_card = 0
        self.count_bad_card = 0
        self.count_bad_search = 0
        self.flag = True

    def run(self):
        self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]')
        sleep(self.parent.device.time_action)
        result = self.parent.device.browser.find_elements(By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div[2]/div/h2')
        if len(result) != 0 and result[0].text == 'No results found':
            self.parent.device.clickButton('/html/body/main/section/section/div[1]/button[1]')
            self.count_bad_search += 1
            if self.count_bad_search >= self.parent.data.bad_search_count:
                self.run_to_post_process()
            else:
                self.run()
        else:
            if self.parent.data.type_bid == 'Bid':
                thread = MyThreadForBid(self)
                thread.run()
            else:
                thread = MyThread(self)
                thread.run()

    def run_to_transfer_targets_for_bid_strategy(self):
        self.parent.device.clickButton('/html/body/main/section/nav/button[3]')
        self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[4]/div[2]')
        if self.parent.data.check == 0:
            thread = MyThreadForBid(self)
            thread.run_to_active_bids()
        else:
            thread = MyThreadForBid(self)
            thread.run_to_won_items()

    def run_to_post_process(self):
        if self.parent.data.post_process_action[0]:
            if self.parent.data.type_post_process == 0:
                self.parent.device.clickButton('/html/body/main/section/nav/button[1]')
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[1]/div[1]')
                parent = self.parent.device.browser.find_element(By.XPATH,
                                                           '/html/body/main/section/section/div[2]/div/div/section[1]/section/ul')
                result = parent.find_elements(By.CLASS_NAME, 'listFUTItem')  # active Bids
                while len(result) != 0:
                    self.parent.data.function_for_post_process(result[0])
                    try:
                        parent = self.parent.device.browser.find_element(By.XPATH,
                                                                     '/html/body/main/section/section/div[2]/div/div/section[1]/section/ul')
                    except Exception:
                        break
                    result = parent.find_elements(By.CLASS_NAME, 'listFUTItem')

            elif self.parent.data.type_post_process == 1:
                self.parent.device.clickButton('/html/body/main/section/nav/button[3]')
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[4]')
                try:
                    self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div/section[4]/header/button')
                except Exception:
                    pass
                parent = self.parent.device.browser.find_element(By.XPATH,
                                                           '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul')
                result = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
                while len(result) != 0:
                    self.parent.data.function_for_post_process(result[0])
                    try:
                        parent = self.parent.device.browser.find_element(By.XPATH,
                                                                         '/html/body/main/section/section/div[2]/div/div/section[1]/section/ul')
                    except Exception:
                        break
                    result = parent.find_elements(By.CLASS_NAME, 'listFUTItem')

            elif self.parent.data.type_post_process == 2:
                self.parent.device.clickButton('/html/body/main/section/nav/button[3]')
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[3]/div[2]')
                if len(self.parent.device.browser.find_elements(By.XPATH,
                                                          '/html/body/main/section/section/div[2]/div/div/div/section[1]/header/button')) != 0:
                    try:
                        self.parent.device.clickButton(
                        '/html/body/main/section/section/div[2]/div/div/div/section[1]/header/button')
                    except Exception:
                        pass
                parent = self.parent.device.browser.find_element(By.XPATH,
                                                           '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul')
                result = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
                while len(result) != 0:
                    self.parent.data.function_for_post_process(result[0])
                    try:
                        parent = self.parent.device.browser.find_element(By.XPATH,
                                                                         '/html/body/main/section/section/div[2]/div/div/section[1]/section/ul')
                    except Exception:
                        break
                    result = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
            self.parent.data.post_process_action = (False, None)
            strategy = StrategyFromEndSell(self.parent)
            strategy.stop(self)
        else:
            strategy = StrategyFromEndSell(self.parent)
            strategy.stop(self)


class MyThread(Thread):
    def __init__(self, sell_obj):
        super(MyThread, self).__init__()
        self.sell_obj = sell_obj

    def run(self):
        result = self.sell_obj.parent.device.parseResultByClass('listFUTItem')
        sleep(self.sell_obj.parent.device.time_action)
        i = 0
        while self.sell_obj.count_bought_card < self.sell_obj.parent.data.countBets and \
                self.sell_obj.count_bad_card < self.sell_obj.parent.data.countBadBets and len(result) != 0:
            flag = self.sell_obj.parent.data.function_for_main_strategy(result[i])
            if flag:
                self.sell_obj.count_bought_card += 1
            else:
                self.sell_obj.count_bad_card += 1
            i += self.sell_obj.parent.data.gap_count
        if self.sell_obj.count_bought_card >= self.sell_obj.parent.data.countBets:
            self.sell_obj.run_to_post_process()
        elif self.sell_obj.count_bad_card >= self.sell_obj.parent.data.countBadBets:
            self.sell_obj.parent.data.function_for_bad_end_strategy(self.sell_obj)  # подумать над сохранением потока или обьекта sell


class MyThreadForBid(Thread): # производит ставки на странице с результатами на странице после фильтров

    def __init__(self, sell_obj):
        super(MyThreadForBid, self).__init__()
        self.sell_obj = sell_obj

    def run(self):
        sleep(self.sell_obj.parent.device.time_action)
        result = self.sell_obj.parent.device.parseResultByClass('listFUTItem')
        i = 0
        while self.sell_obj.count_bought_card < self.sell_obj.parent.data.countBets and \
                self.sell_obj.count_bad_card < self.sell_obj.parent.data.countBadBets and len(result) != 0:
            flag = self.sell_obj.parent.data.function_for_bid_process(result[i])
            if flag:
                self.sell_obj.count_bought_card += 1
            else:
                self.sell_obj.count_bad_card += 1
            i += self.sell_obj.parent.data.gap_count
        if self.sell_obj.count_bought_card >= self.sell_obj.parent.data.countBets:
            self.sell_obj.run_to_transfer_targets_for_bid_strategy()
        elif self.sell_obj.count_bad_card >= self.sell_obj.parent.data.countBadBets:
            self.sell_obj.parent.data.function_for_bad_end_strategy(self.sell_obj) # подумать над сохранением потока или обьекта sell

    def run_to_active_bids(self):
        parent = self.sell_obj.parent.device.browser.find_element(By.XPATH,
                                                         '/html/body/main/section/section/div[2]/div/div/div/section[1]/ul')
        try:
            cards = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
        except Exception:
            cards = []
        while len(cards) != 0:
            for card in cards:
                try:
                    WebDriverWait(self.sell_obj.parent.device, 0.5).until(
                        self.sell_obj.parent.device.clickButton(card)
                    )
                except Exception:
                    continue
                if len(card.find_elements(By.CSS_SELECTOR, 'li.listFUTItem.outbid')) != 0:
                    price = int(self.sell_obj.parent.device.find_element(By.XPATH,
                                                          '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[1]/div/div[2]/span[2]').text.replace(
                        ',', ''))
                    try:
                        WebDriverWait(self.sell_obj.parent.device, 0.5).until(
                            self.sell_obj.parent.device.inputForm(
                                '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div/input',
                                str(price + 50))
                        )
                    except Exception:
                        continue
                    try:
                        WebDriverWait(self.sell_obj.parent.device, 0.5).until(
                            self.sell_obj.parent.device.clickButton(
                                '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/button[1]')
                        )
                    except Exception:
                        continue
            parent = self.sell_obj.parent.device.browser.find_element(By.XPATH,
                                                       '/html/body/main/section/section/div[2]/div/div/div/section[1]/ul')
            try:
                cards = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
            except Exception:
                cards = []
        thread = MyThreadForBid(self.sell_obj)
        thread.run_to_won_items()

    def run_to_won_items(self):
        parent = self.sell_obj.parent.device.browser.find_element(By.XPATH,
                                                   '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul')
        cards = parent.find_elements(By.CLASS_NAME, 'listFUTItem')  # won items
        count = 0
        for card in cards:
            flag = self.sell_obj.parent.data.function_for_main_strategy(card)
            count += 1
        if count >= self.sell_obj.parent.data.countBets:
            if self.sell_obj.data.post_process_action[0]:
                self.sell_obj.run_to_post_process()
            else:
                strategy = StrategyFromEndSell(self.sell_obj.parent)
                strategy.stop(self.sell_obj)
        else:
            self.sell_obj.parent.data.countBets -= count
            self.sell_obj.count_bought_card = 0
            self.sell_obj.count_bad_card = 0
            self.sell_obj.parent.device.clickButton('/html/body/main/section/nav/button[3]')
            self.sell_obj.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[2]/div[2]')
            self.sell_obj.run()