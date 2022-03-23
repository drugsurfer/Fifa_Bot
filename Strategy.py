from tkinter import *
from ActionWithSite import Browser
from selenium.webdriver.common.by import By
from time import sleep
import Window


class StrategyForPostProcess:

    def __init__(self, parent):
        self.parent = parent
        self.step_for_bid = 0
        self.step_for_buy = 0

        self.reference_for_unallocated = {0: self.sell_for_compare_price,
                                          1: self.transfer_on_price,
                                          2: self.send_to_transfer_list,
                                          3: self.send_to_club}
        self.reference_for_transfer_targets = {0: self.sell_for_compare_price,
                                               1: self.transfer_on_price,
                                               2: self.send_to_transfer_list,
                                               3: self.send_to_club}
        self.reference_for_transfer_list = {0: self.sell_for_compare_price,
                                            1: self.transfer_on_price,
                                            2: self.set_step_price}

    def get_unallocated_method(self, index):
        return self.reference_for_unallocated[index]

    def get_transfer_targets_method(self, index):
        return self.reference_for_transfer_targets[index]

    def get_transfer_list_method(self, index):
        return self.reference_for_transfer_list[index]

    def get_last_price(self):
        return self.set_last_price

    def parse_str(self, text):
        return text.replace(',', '')

    def sell_for_compare_price(self, cardObj):
        self.parent.device.clickButton(cardObj)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        sleep(3)
        elements = panel.find_elements(By.TAG_NAME, 'button')
        for element in elements:
            span = element.find_elements(By.TAG_NAME, 'span')
            if len(span) != 0:
                for s in span:
                    if s.text == 'Compare Price':
                        element.click()
        sleep(3)
        parent = self.parent.device.browser.find_element(By.CLASS_NAME, 'paginated-item-list')
        cards = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
        min_price = 1000000
        for card in cards:
            price_text = card.find_element(By.XPATH, './/div[1]/div[2]/div[3]/span[2]')
            price = self.parse_str(price_text.text)
            if int(price) < min_price:
                min_price = int(price)
        b = self.parent.device.browser.find_element(By.CLASS_NAME, 'navbar-style-secondary')
        b.find_element(By.CLASS_NAME, 'ut-navigation-button-control').click()
        sleep(3)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        panel.find_element(By.CLASS_NAME, 'accordian').click()
        sleep(3)
        row = panel.find_elements(By.CLASS_NAME, 'ut-numeric-input-spinner-control')
        input_s = row[1].find_element(By.CLASS_NAME, 'numericInput')
        input_s.click()
        sleep(3)
        input_s.send_keys(str(min_price))
        sleep(3)
        panel.find_element(By.CLASS_NAME, 'call-to-action').click()
        sleep(3)

    def transfer_on_price(self, cardObj):
        self.parent.device.clickButton(cardObj)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        sleep(1)
        panel.find_element(By.CLASS_NAME, 'accordian').click()
        card = panel.find_element(By.CLASS_NAME, 'boughtPrice')
        price = card.find_element(By.CLASS_NAME, 'boughtPriceValue').text
        row = panel.find_elements(By.CLASS_NAME, 'ut-numeric-input-spinner-control')
        input_s = row[1].find_element(By.CLASS_NAME, 'numericInput')
        input_s.click()
        sleep(1)
        input_s.send_keys(str(price))
        sleep(1)
        panel.find_element(By.CLASS_NAME, 'call-to-action').click()
        sleep(1)

    def send_to_transfer_list(self, cardObj):
        self.parent.device.clickButton(cardObj)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        sleep(1)
        elements = panel.find_elements(By.TAG_NAME, 'button')
        for element in elements:
            span = element.find_elements(By.TAG_NAME, 'span')
            if len(span) != 0:
                for s in span:
                    if s.text == 'Send to Transfer List':
                        element.click()

    def send_to_club(self, cardObj):
        self.parent.device.clickButton(cardObj)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        sleep(1)
        elements = panel.find_elements(By.TAG_NAME, 'button')
        for element in elements:
            span = element.find_elements(By.TAG_NAME, 'span')
            if len(span) != 0:
                for s in span:
                    if s.text == 'Send to My Club':
                        element.click()
                        sleep(1)

    def set_last_price(self, cardObj):
        self.parent.device.clickButton(cardObj)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        sleep(1)
        panel.find_element(By.CLASS_NAME, 'accordian').click()
        sleep(1)
        panel.find_element(By.CLASS_NAME, 'call-to-action').click()
        sleep(1)

    def set_step_price(self, cardObj):
        self.parent.device.clickButton(cardObj)
        panel = self.parent.device.browser.find_element(By.CLASS_NAME, 'DetailPanel')
        sleep(1)
        panel.find_element(By.CLASS_NAME, 'accordian').click()
        sleep(1)
        row = panel.find_elements(By.CLASS_NAME, 'ut-numeric-input-spinner-control')
        for i in range(self.step_for_bid):
            row[0].find_element(By.CLASS_NAME, 'increment-value')
            sleep(0.5)
        for i in range(self.step_for_buy):
            row[1].find_element(By.CLASS_NAME, 'increment-value')
            sleep(0.5)
        panel.find_element(By.CLASS_NAME, 'call-to-action').click()
        sleep(1)


class StrategyForMainProcess:
    def __init__(self, parent):
        self.parent = parent
        self.user_price = 0
        self.reference = {0: self.sell_for_compare_price,
                          1: self.transfer_on_price,
                          2: self.user_price_on_transfer,
                          3: self.send_to_transfer_list,
                          4: self.send_to_club,
                          5: self.send_to_unallocated}

    def parseStr(self, text):
        return text.replace(',', '')

    def bid_trading_min(self, cardObj):
        self.parent.device.clickButton(cardObj)
        price = self.parseStr(cardObj.find_element(By.CLASS_NAME, 'currency-coins').text)
        if int(price) > self.parent.data.maxBid:
            price = str(self.parent.data.maxBid)
        if self.parent.device.onClickableElement(
                '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]'):
            self.parent.device.inputForm(
                '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input',
                price)
            if self.parent.device.onClickableElement(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]'):
                self.parent.device.clickButton(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]')
                if self.parent.device.search_attention('div.Notification.negative'):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def bid_trading_max(self, cardObj):
        self.parent.device.clickButton(cardObj)
        if self.parent.device.onClickableElement('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]'):
            self.parent.device.inputForm('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input', str(self.parent.data.maxBid))
            if self.parent.device.onClickableElement('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]'):
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]')
                if self.parent.device.search_attention('div.Notification.negative'): # /html/body/div[5]
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def sell_for_compare_price(self, cardObj): # предусмотреть ошибки вылезающие на экране
        if self.parent.data.type_bid == 'Bid':
            self.parent.device.clickButton(cardObj)
            self.parent.device.clickButton(
                '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[3]/button[9]')
            parent = self.parent.device.browser.find_element(By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div[2]/section/div[2]/ul')
            cards = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
            min_price = 1000000
            for card in cards:
                price_text = card.find_element(By.XPATH, './/div[1]/div[2]/div[3]/span[2]')
                price = self.parseStr(price_text.text)
                if int(price) < min_price:
                    min_price = int(price)
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div[1]/button')
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[2]/div[1]/button')
            self.parent.device.inputForm('/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[2]/input', str(min_price))
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[2]/div[2]/button')
        else:
            self.parent.device.clickButton(cardObj)
            if self.parent.device.onClickableElement('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[3]/button[2]') # нажатие на кнопку ComparePrice
                parent = self.parent.device.browser.find_element(By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/section/div[2]/ul')
                cards = parent.find_elements(By.CLASS_NAME, 'listFUTItem')
                min_price = 1000000
                for card in cards:
                    price_text = card.find_element(By.XPATH, './/div[1]/div[2]/div[3]/span[2]')
                    price = self.parseStr(price_text.text)
                    if int(price) < min_price:
                        min_price = int(price)
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div[1]/button')
                if self.parent.device.onClickableElement('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                    self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]') # покупаем карту по BuyNowPrice
                    element = self.parent.device.browser.find_elements(By.XPATH, '/html/body/div[4]/section/header/h1')
                    if len(element) != 0 and element[0].text == 'New Items Full':
                        self.parent.device.clickButton(
                            '/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                        return True
                    else:
                        self.parent.device.clickButton('/html/body/div[4]/section/div/div/button[1]') # подтверждение покупки
                        if self.parent.device.search_attention('div.Notification.negative'):
                            # здесь карта уже куплена нажимаем на List Transfer Market
                            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[1]/button')
                            self.parent.device.inputForm('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input', str(min_price))
                            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button')
                            return True
                        else:
                            return False
                else:
                    return False
            else:
                return False

    def transfer_on_price(self, cardObj):
        self.parent.device.clickButton(cardObj)
        if self.parent.data.type_bid == 'Bid':
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[1]/button')
            card = cardObj.find_element(By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li/div/div[2]/div[3]/span[2]')
            price = card.text
            self.parent.device.inputForm(
                        '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input',
                        str(price))
            self.parent.device.clickButton(
                        '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/button')
        else:
            if self.parent.device.onClickableElement(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                card = cardObj.find_element(By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[1]/div/ul/li[1]/div/div[2]/div[3]/span[2]')
                price = card.text
                self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]')# покупаем карту по BuyNowPrice
                element = self.parent.device.browser.find_elements(By.XPATH, '/html/body/div[4]/section/header/h1')
                if len(element) != 0 and element[0].text == 'New Items Full':
                    self.parent.device.clickButton(
                        '/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    return True
                else:
                    self.parent.device.clickButton('/html/body/div[4]/section/div/div/button[1]')# подтверждение покупки
                    if self.parent.device.search_attention('div.Notification.negative'):
                        self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[1]/button')
                        self.parent.device.inputForm(
                            '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input',
                            str(price))
                        self.parent.device.clickButton(
                            '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button')
                        return True
                    else:
                        return False
            else:
                return False

    def user_price_on_transfer(self, cardObj):
        self.parent.device.clickButton(cardObj)
        if self.parent.data.type_bid == 'Bid':
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[1]/button')
            if self.user_price == 0:
                card = self.parent.device.browser.find_element(By.XPATH,
                                                         '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[1]/div[2]/div/span[2]')
                price = card.text
            else:
                price = self.user_price
            self.parent.device.inputForm(
                    '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input',
                    str(price))
            self.parent.device.clickButton(
                    '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/button')
        else:
            if self.user_price == 0:
                card = self.parent.device.browser.find_element(By.XPATH,
                                                     '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]')
                price = card.text
            else:
                price = self.user_price
            if self.parent.device.onClickableElement(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                self.parent.device.clickButton(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]')  # покупаем карту по BuyNowPrice
                element = self.parent.device.browser.find_elements(By.XPATH, '/html/body/div[4]/section/header/h1')
                if len(element) != 0 and element[0].text == 'New Items Full':
                    self.parent.device.clickButton(
                        '/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    return True
                else:
                    self.parent.device.clickButton('/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    if self.parent.device.search_attention('div.Notification.negative'):
                        self.parent.device.clickButton(
                            '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[1]/button')
                        self.parent.device.inputForm(
                            '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input',
                            str(price))
                        self.parent.device.clickButton(
                            '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button')
                        return True
                    else:
                        return False
            else:
                return False

    def send_to_transfer_list(self, cardObj):
        self.parent.device.clickButton(cardObj)
        if self.parent.data.type_bid == 'Bid':
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[3]/button[8]')
        else:
            if self.parent.device.onClickableElement(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                self.parent.device.clickButton(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]')  # покупаем карту по BuyNowPrice
                element = self.parent.device.browser.find_elements(By.XPATH, '/html/body/div[4]/section/header/h1')
                if len(element) != 0 and element[0].text == 'New Items Full':
                    self.parent.device.clickButton(
                        '/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    return True
                else:
                    self.parent.device.clickButton('/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    if self.parent.device.search_attention('div.Notification.negative'):
                        self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[3]/button[8]')
                        return True
                    else:
                        return False
            else:
                return False

    def send_to_club(self, cardObj):
        self.parent.device.clickButton(cardObj)
        if self.parent.data.type_bid == 'Bid':
            self.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[3]/button[6]')
        else:
            if self.parent.device.onClickableElement(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                self.parent.device.clickButton(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]')  # покупаем карту по BuyNowPrice
                element = self.parent.device.browser.find_elements(By.XPATH, '/html/body/div[4]/section/header/h1')
                if len(element) != 0 and element[0].text == 'New Items Full':
                    self.parent.device.clickButton(
                        '/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    return True
                else:
                    self.parent.device.clickButton('/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    if self.parent.device.search_attention('div.Notification.negative'):
                        self.parent.device.clickButton(
                            '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[3]/button[6]')
                        return True
                    else:
                        return False
            else:
                return False

    def send_to_unallocated(self, cardObj):
        if self.parent.data.type_bid != 'Bid':
            self.parent.device.clickButton(cardObj)
            if self.parent.device.onClickableElement(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]'):
                self.parent.device.clickButton(
                    '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]')  # покупаем карту по BuyNowPrice
                element = self.parent.device.browser.find_elements(By.XPATH, '/html/body/div[4]/section/header/h1')
                if len(element) != 0 and element[0].text == 'New Items Full':
                    self.parent.device.clickButton(
                        '/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    return True
                else:
                    self.parent.device.clickButton('/html/body/div[4]/section/div/div/button[1]')  # подтверждение покупки
                    if self.parent.device.search_attention('div.Notification.negative'):
                        return True
                    else:
                        return False
            else:
                return False


class StrategyFromEndSell:

    def __init__(self, parent):
        self.parent = parent
        self.reference = {0: self.pause,
                          1: self.stop,
                          2: self.research,
                          3: self.research_basic}

    def pause(self, sell_obj):
        if sell_obj.count_bought_card >= sell_obj.parent.data.countBets:
            sell_obj.count_bought_card = 0
        if sell_obj.count_bad_card >= sell_obj.parent.data.countBadBets:
            sell_obj.count_bad_card = 0
        sell_obj.parent.device.clickButton('/html/body/main/section/nav/button[3]')
        sell_obj.parent.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[2]/div[2]')
        sleep(sell_obj.parent.data.time_timeout)
        sell_obj.run()

    def stop(self, sell_obj):
        if not sell_obj.parent.data.post_process_action[0]:
            sell_obj.parent.root.destroy()
            sell_obj.parent.root.update()
            sell_obj.parent.device.browser.quit()
            w = Window.Window(750, 500)
            w.run()
        else:
            sell_obj.run_to_post_process()

    def research(self, sell_obj):
        sell_obj.parent.device.clickButton('/html/body/main/section/section/div[1]/button[1]')
        self.step_by_bid(sell_obj)
        sell_obj.count_bad_card = 0
        sell_obj.run()

    def research_basic(self, sell_obj):
        sell_obj.parent.device.clickButton('/html/body/main/section/section/div[1]/button[1]')
        self.step_by_bid(sell_obj)
        sell_obj.count_bad_card = 0
        sell_obj.parent.device.clickHiddenButton(
            '/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[5]/div/ul/li[2]',
            '/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[5]/div/div')
        sell_obj.run()

    def step_by_bid(self, sell_obj):
        if sell_obj.flag:
            sell_obj.parent.device.clickButton(
                '/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/button[2]')
            sell_obj.flag = False
        else:
            sell_obj.parent.device.clickButton(
                '/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/button[1]')
            sell_obj.flag = True