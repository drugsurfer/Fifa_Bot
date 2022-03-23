from tkinter import *
from ActionWithSite import Browser
import os.path
import pickle
import time
import data
from Filter import Filter
from Strategy import StrategyForPostProcess, StrategyForMainProcess, StrategyFromEndSell
from Sell import Sell
'''
1)  доделать отправку кода
2)  доделать pause, stop, research в Strategy
'''


class Window:
    def __init__(self, WIDTH, HEIGHT, title="Fifa_Bot", resiazable=(True, True)):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{WIDTH}x{HEIGHT}+200+200")
        self.root.resizable(resiazable[0], resiazable[1])
        self.font = ("Calibri", 15, "bold")

        self.button_start = Button(self.root, command=lambda: self.run_aplication(), text='Start',
                                   width=6, height=2, bg='black', fg='red', font='arial 14')
        self.button_bid_price = Button(self.root, command=lambda: self.set_bid_buy(), text='BidPrice',
                                       width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_buy_now_price = Button(self.root, command=lambda: self.set_buy_now_price_buy(), text='BuyNowPrice',
                                           width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_for_autorization = Button(self.root, command=lambda: self.set_data_of_autorization(),
                                              text='Authorization',
                                              width=8, height=2, bg='black', fg='red', font='arial 14')
        self.button_apply_code = Button(self.root, command=lambda: self.set_code(), text='Apply Code',
                                        width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_for_card_player = Button(self.root, command=lambda: self.card_player(), text='CardPlayer',
                                             width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_for_change_position = Button(self.root, command=lambda: self.change_position(),
                                                 text='ChangePosition',
                                                 width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_for_type_style = Button(self.root, command=lambda: self.type_style(), text='TypeStyle',
                                                 width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_reset = Button(self.root, command=lambda: None, text='Reset',
                                                 width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_search = Button(self.root, command=lambda: None, text='Search',
                                                 width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_enter = Button(self.root, command=lambda: self.filter_count(), text='Search',
                                                 width=10, height=2, bg='black', fg='red', font='arial 14')
        self.button_set_last_price = Button(self.root, command=lambda: self.set_last_price(), text='Last Price',
                                                 width=10, height=2, bg='black', fg='red', font='arial 14')

        self.login = Entry(self.root, width=15)
        self.login.insert(0, 'axecapital10@yandex.ru')
        self.password = Entry(self.root, width=15)
        self.password.insert(0, 'ClassikofFifa7')
        self.code = Entry(self.root, width=15)

        self.min = Entry(self.root, width=15)
        self.max = Entry(self.root, width=15)
        self.min.insert(0, 'Min')
        self.max.insert(0, 'Max')

        self.Name = Entry(self.root, width=15)
        self.Name.insert(0, 'Name')

        self.QualityList = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.Position = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.Nationality = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.Club = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.Rarity = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.ChemistryStyle = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.League = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.ChemistryStyle = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)

        self.checkStartMax = Radiobutton(self.root, text="Начинаем с минимальной", value=1,
                                         command=lambda: self.set_check(0))
        self.checkStartMin = Radiobutton(self.root, text="Сразу максимальная", value=2,
                                         command=lambda: self.set_check(1))

        self.count_good_bets = Entry(self.root, width=15)
        self.count_good_bets.insert(0, 'count_good_bets')
        self.count_bad_bets = Entry(self.root, width=15)
        self.count_bad_bets.insert(0, 'count_bad_bets')

        self.gap_count = Entry(self.root, width=15)
        self.gap_count.insert(0, 'gap_count')

        self.bad_search_count = Entry(self.root, width=15)
        self.bad_search_count.insert(0, 'bad_search_count')

        self.time_to_timeout = Entry(self.root, width=15)
        self.time_to_timeout.insert(0, 'time_to_timeout')

        self.time_timeout = Entry(self.root, width=15)
        self.time_timeout.insert(0, 'time_timeout')

        self.time_to_filters = Entry(self.root, width=15)
        self.time_to_filters.insert(0, 'time_to_filters')

        self.time_to_transfer = Entry(self.root, width=15)
        self.time_to_transfer.insert(0, 'time_to_transfer')

        self.step_for_bid = Entry(self.root, width=15)
        self.step_for_bid.insert(0, 'step_for_bid')

        self.step_for_buy = Entry(self.root, width=15)
        self.step_for_buy.insert(0, 'step_for_buy')

        self.max_user_Bid = Entry(self.root, width=15)
        self.max_user_Bid.insert(0, 'max_user_bid')
        self.user_price = Entry(self.root, width=15)
        self.user_price.insert(0, 'user_price')

        self.lst_action_end_bets = Listbox(self.root, height=5, width=25, selectmode=SINGLE, exportselection=0)
        self.lst_action_end_bets.insert(END, 'pause')
        self.lst_action_end_bets.insert(END, 'stop')

        self.lst_action_end_bad_bets = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.lst_action_end_bad_bets.insert(END, 'pause')
        self.lst_action_end_bad_bets.insert(END, 'stop')
        self.lst_action_end_bad_bets.insert(END, 'research')
        self.lst_action_end_bad_bets.insert(END, 'research_basic')

        self.before_game_action_lst = Listbox(self.root, height=5, width=15, selectmode=SINGLE, exportselection=0)
        self.before_game_action_lst.insert(END, 'распределение предметов из списка нераспределенных')
        self.before_game_action_lst.insert(END, 'распределения вкладки трансферные цели')
        self.before_game_action_lst.insert(END, 'распределения вкладки список продаж')
        self.check = 10
        self.data = data.Data()
        self.device = Browser()

    def run(self):
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        self.max_user_Bid.grid_forget()
        self.lst_action_end_bets.grid_forget()
        self.lst_action_end_bad_bets.grid_forget()
        self.user_price.grid_forget()
        self.button_set_last_price.grid_forget()
        self.step_for_bid.grid_forget()
        self.step_for_buy.grid_forget()
        self.before_game_action_lst.grid_forget()
        self.gap_count.grid_forget()
        self.bad_search_count.grid_forget()
        self.time_to_timeout.grid_forget()
        self.time_timeout.grid_forget()
        self.time_to_filters.grid_forget()
        self.time_to_transfer.grid_forget()
        self.button_enter.grid_forget()
        self.count_good_bets.grid_forget()
        self.count_bad_bets.grid_forget()
        self.checkStartMin.grid_forget()
        self.checkStartMax.grid_forget()
        self.button_reset.grid_forget()
        self.button_search.grid_forget()
        self.min.grid_forget()
        self.max.grid_forget()
        self.Name.grid_forget()
        self.QualityList.grid_forget()
        self.Position.grid_forget()
        self.Nationality.grid_forget()
        self.Club.grid_forget()
        self.Rarity.grid_forget()
        self.ChemistryStyle.grid_forget()
        self.League.grid_forget()
        self.ChemistryStyle.grid_forget()
        self.button_bid_price.grid_forget()
        self.button_buy_now_price.grid_forget()
        self.button_for_autorization.grid_forget()
        self.button_apply_code.grid_forget()
        self.button_for_card_player.grid_forget()
        self.button_for_change_position.grid_forget()
        self.button_for_type_style.grid_forget()
        self.button_start.grid(row=0, column=0)

    def run_aplication(self):
        self.button_start.grid_forget()
        self.button_for_autorization.grid(row=0, column=2)
        self.login.grid(row=0, column=0)
        self.password.grid(row=1, column=0)

        self.device.getInfo('https://www.ea.com/fifa/ultimate-team/web-app/')
        if not(self.check_cookie()):
            self.button_for_autorization.config(command=lambda: self.set_data_of_autorization_with_code())

    def set_data_of_autorization_with_code(self):
        self.device.inputForm('/html/body/div[1]/div[2]/section/div[1]/form/div[1]/div[1]/div[1]/input',
                              self.login.get())
        self.device.inputForm('/html/body/div[1]/div[2]/section/div[1]/form/div[1]/div[2]/input', self.password.get())
        self.device.clickAutorizationButton('/html/body/div[1]/div[2]/section/div[1]/form/div[6]/a')
        time.sleep(3)
        self.device.clickButton('/html/body/div/form/div/section/a[2]')
        self.login.grid_forget()
        self.password.grid_forget()
        self.button_for_autorization.grid_forget()
        self.button_apply_code.grid(row=0, column=1)
        self.code.grid(row=0, column=0)

    def check_cookie(self):
        if os.path.exists('cookies'):
            for cookie in pickle.load(open('cookies', 'rb')):
                self.device.browser.add_cookie(cookie)
            time.sleep(1)
            self.device.browser.refresh()
            time.sleep(5)
            self.device.clickButton('/html/body/main/div/div/div/button[1]')
            return True
        else:   # dont have cookie
            time.sleep(5)
            self.device.clickButton('/html/body/main/div/div/div/button[1]')
            return False

    def set_check(self, value):
        self.check = value

    def set_data_of_autorization(self):
        self.device.inputForm('/html/body/div[1]/div[2]/section/div[1]/form/div[1]/div[1]/div[1]/input',
                              self.login.get())
        self.device.inputForm('/html/body/div[1]/div[2]/section/div[1]/form/div[1]/div[2]/input', self.password.get())
        self.device.clickAutorizationButton('/html/body/div[1]/div[2]/section/div[1]/form/div[6]/a')
        time.sleep(3)
        self.login.grid_forget()
        self.password.grid_forget()
        self.button_for_autorization.grid_forget()
        time.sleep(8)
        self.button_for_card_player.grid(row=0, column=0)
        self.button_for_change_position.grid(row=1, column=0)
        self.button_for_type_style.grid(row=2, column=0)

    def set_code(self):
        self.device.inputForm('/html/body/div[1]/form/div/section/div[2]/div/input', self.code.get())
        self.device.clickButton('/html/body/div[1]/form/div/section/div[5]/a')
        self.button_apply_code.grid_forget()
        self.code.grid_forget()
        time.sleep(10)
        pickle.dump(self.device.browser.get_cookies(), open("cookies", "wb"))
        self.button_for_card_player.grid(row=0, column=0)
        self.button_for_change_position.grid(row=1, column=0)
        self.button_for_type_style.grid(row=2, column=0)

    def type_button_off(self):
        self.button_for_card_player.grid_forget()
        self.button_for_change_position.grid_forget()
        self.button_for_type_style.grid_forget()
        self.button_bid_price.grid(row=0, column=0)
        self.button_buy_now_price.grid(row=1, column=0)

    def card_player(self):
        self.device.clickButton('/html/body/main/section/nav/button[3]')
        self.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[2]/div[2]')
        self.data.type_buy_object = 'CP'
        self.type_button_off()

    def change_position(self):
        self.device.clickButton('/html/body/main/section/nav/button[3]')
        self.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[2]/div[2]')
        self.device.clickButton('/html/body/main/section/section/div[2]/div/div[1]/div/button[4]')
        self.data.type_buy_object = 'CPos'
        self.type_button_off()

    def type_style(self):
        self.device.clickButton('/html/body/main/section/nav/button[3]')
        self.device.clickButton('/html/body/main/section/section/div[2]/div/div/div[2]/div[2]')
        self.device.clickHiddenButton(
            '/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/ul/li[2]',
            '/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div')
        self.data.type_buy_object = 'TS'
        self.type_button_off()

    def set_bid_buy(self):
        self.button_bid_price.grid_forget()
        self.button_buy_now_price.grid_forget()
        self.data.type_bid = 'Bid'
        filter_window = Filter(self)
        self.button_search.config(command=lambda: filter_window.input_data())

    def set_buy_now_price_buy(self):
        self.button_bid_price.grid_forget()
        self.button_buy_now_price.grid_forget()
        self.data.type_bid = 'Buy'
        self.filter_window = Filter(self)
        self.button_search.config(command=lambda: self.filter_window.input_data())

    def filter_count(self):
        if self.count_good_bets.get() != 'count_good_bets':
            self.data.set_count_bets(int(self.count_good_bets.get()))
        if self.count_bad_bets.get() != 'count_bad_bets':
            self.data.set_count_bad_bets(int(self.count_bad_bets.get()))

        if self.gap_count.get() != 'gap_count':
            self.data.set_gap_count(int(self.gap_count.get()))
        if self.bad_search_count.get() != 'bad_search_count':
            self.data.set_bad_search_count(int(self.bad_search_count.get()))
        if self.time_to_timeout.get() != 'time_to_timeout':
            self.data.set_time_to_timeout(int(self.time_to_timeout.get()))
        if self.time_timeout.get() != 'time_timeout':
            self.data.set_time_timeout(int(self.time_timeout.get()))
        if self.time_to_filters.get() != 'time_to_filters':
            self.data.set_time_to_filters(int(self.time_to_filters.get()))
        if self.time_to_transfer.get() != 'time_to_transfer':
            self.data.set_time_to_transfer(int(self.time_to_transfer.get()))
        if self.data.type_bid == 'Bid' and self.data.check == 0:
            if self.max_user_Bid.get() != 'max_user_bid':
                self.data.set_max_bid(int(self.max_user_Bid.get()))
            self.max_user_Bid.grid_forget()
        self.device.time_action = self.data.time_to_filters
        self.filter_window.set_filters()
        self.device.time_action = self.data.time_to_transfer
        self.count_good_bets.grid_forget()
        self.count_bad_bets.grid_forget()
        self.button_enter.grid_forget()
        self.gap_count.grid_forget()
        self.bad_search_count.grid_forget()
        self.time_to_timeout.grid_forget()
        self.time_timeout.grid_forget()
        self.time_to_filters.grid_forget()
        self.time_to_transfer.grid_forget()
        self.lst_action_end_bets.grid(row=0, column=0)
        self.lst_action_end_bad_bets.grid(row=0, column=1)
        self.button_enter.config(command=lambda: self.action_from_end_strategy())
        self.button_enter.grid(row=0, column=2)

    def action_from_end_strategy(self):
        act_good = self.lst_action_end_bets.curselection()
        act_bad = self.lst_action_end_bad_bets.curselection()
        strategy = StrategyFromEndSell(self)
        if len(act_good) != 0:
            self.data.function_for_end_strategy = strategy.reference[act_good[0]]
        if len(act_bad) != 0:
            self.data.function_for_bad_end_strategy = strategy.reference[act_bad[0]]
        self.lst_action_end_bets.grid_forget()
        self.lst_action_end_bad_bets.grid_forget()
        self.before_game_action_lst.grid(row=0, column=0)
        self.button_enter.config(command=lambda: self.set_post_process_action())

    def set_post_process_action(self):
        act = self.before_game_action_lst.curselection()
        if len(act) != 0:
            self.data.post_process_action = (True, act[0])
            self.data.type_post_process = act[0]
        self.before_game_action_lst.grid_forget()
        self.button_enter.grid_forget()
        for i in range(self.before_game_action_lst.size()):
            self.before_game_action_lst.delete(i)
        if self.data.post_process_action[0]:
            if self.data.post_process_action[1] == 0:
                self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по минимальной рыночной цене')
                self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по цене относительно цены покупки')
                self.before_game_action_lst.insert(END, 'Отправить карту в список продаж')
                self.before_game_action_lst.insert(END, 'Отправить карту в клуб')
                self.before_game_action_lst.delete(0)
                self.button_enter.config(command=lambda: self.post_process_unallocated())
            elif self.data.post_process_action[1] == 1:
                self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по минимальной рыночной цене')
                self.before_game_action_lst.insert(END,
                                            'выставить карту на трансферный рынок по цене относительно цены покупки')
                self.before_game_action_lst.insert(END, 'Отправить карту в список продаж')
                self.before_game_action_lst.insert(END, 'Отправить карту в клуб ')
                self.before_game_action_lst.delete(0)
                self.button_enter.config(command=lambda: self.post_process_transfer_targets())
            else:
                self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по минимальной рыночной цене')
                self.before_game_action_lst.insert(END,
                                            'выставить карту на трансферный рынок по цене относительно цены покупки')
                self.before_game_action_lst.insert(END, 'выставить задав отклонение')
                self.before_game_action_lst.delete(0)
                self.button_enter.config(command=lambda: self.post_process_transfer_list())
            self.before_game_action_lst.grid(row=0, column=0)
            self.button_set_last_price.grid(row=0, column=1)
            self.button_enter.grid(row=1, column=1)
        else:
            self.set_main_strategy()

    def post_process_unallocated(self):
        strategy = StrategyForPostProcess(self)
        act = self.before_game_action_lst.curselection()
        self.before_game_action_lst.grid_forget()
        self.button_enter.grid_forget()
        self.button_set_last_price.grid_forget()
        if len(act) != 0:
            self.data.function_for_post_process = strategy.get_unallocated_method(act[0])
        else:
            self.data.post_process_action = (False, None)
        self.set_main_strategy()

    def post_process_transfer_targets(self):
        strategy = StrategyForPostProcess(self)
        act = self.before_game_action_lst.curselection()
        self.before_game_action_lst.grid_forget()
        self.button_set_last_price.grid_forget()
        self.button_enter.grid_forget()
        if len(act) != 0:
            self.data.function_for_post_process = strategy.get_transfer_targets_method(act[0])
        else:
            self.data.post_process_action = (False, None)
        self.set_main_strategy()

    def post_process_transfer_list(self):
        strategy = StrategyForPostProcess(self)
        act = self.before_game_action_lst.curselection()
        self.before_game_action_lst.grid_forget()
        self.button_enter.grid_forget()
        self.button_set_last_price.grid_forget()
        if len(act) != 0:
            if act[0] == 2:
                self.step_for_bid.grid(row=0, column=0)
                self.step_for_buy.grid(row=1, column=0)
                self.button_enter.config(command=lambda: self.set_step_method(strategy))
                self.button_enter.grid(row=0, column=1)
            else:
                self.data.function_for_post_process = strategy.get_transfer_list_method(act[0])
        else:
            self.data.post_process_action = (False, None)
        self.set_main_strategy()

    def set_step_method(self, strategy):
        if self.step_for_bid.get() != 'step_for_bid':
            strategy.step_for_bid = self.step_for_bid.get()
        if self.step_for_buy.get() != 'step_for_buy':
            strategy.step_for_buy = self.step_for_buy.get()
        self.data.post_process_action = (True, strategy.get_transfer_list_method(2))
        self.data.function_for_post_process = strategy.get_transfer_list_method(2)
        self.step_for_buy.grid_forget()
        self.step_for_bid.grid_forget()
        self.button_enter.grid_forget()
        self.button_set_last_price.grid_forget()
        self.set_main_strategy()

    def set_last_price(self):
        strategy = StrategyForPostProcess(self)
        self.data.post_process_action = (True, strategy.get_last_price())
        self.data.function_for_post_process = strategy.get_last_price()
        self.button_set_last_price.grid_forget()
        self.button_enter.grid_forget()
        self.set_main_strategy()

    def set_main_strategy(self):
        for i in range(self.before_game_action_lst.size()):
            self.before_game_action_lst.delete(i)
        self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по минимальной рыночной цене')
        self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по цене относительно цены покупки')
        self.before_game_action_lst.insert(END, 'выставить карту на трансферный рынок по установленной пользователем цене')
        self.before_game_action_lst.insert(END, 'отправить карту в список продаж')
        self.before_game_action_lst.insert(END, 'отправить карту в клуб')
        self.before_game_action_lst.insert(END, 'оставить в нераспределенных')
        if self.data.post_process_action[1] == 0:
            self.before_game_action_lst.delete(0)
            self.before_game_action_lst.delete(0)
        else:
            self.before_game_action_lst.delete(0)
        self.button_enter.config(command=lambda: self.set_strategy_in_data())
        self.before_game_action_lst.grid(row=0, column=0)
        self.button_enter.grid(row=1, column=1)

    def set_strategy_in_data(self):
        act = self.before_game_action_lst.curselection()
        strategy = StrategyForMainProcess(self)
        if self.data.type_bid == 'Bid':
            if self.data.check == 0:
                self.data.function_for_bid_process = strategy.bid_trading_min
            else:
                self.data.function_for_bid_process = strategy.bid_trading_max
        self.data.function_for_main_strategy = strategy.reference[act[0]]
        if act[0] == 2: # установка пользователем цены
            self.user_price.grid(row=0, column=1)
            self.button_enter.config(command=lambda: self.set_user_price(strategy))
        else:
            self.before_game_action_lst.grid_forget()
            self.button_enter.grid_forget()
            self.button_start.config(command=lambda: self.start_sell())
            self.button_start.grid(row=0, column=0)

    def set_user_price(self, strategy):
        if self.user_price.get() != 'user_price':
            strategy.user_price = self.user_price.get()
        else:
            strategy.user_price = 500
        self.user_price.grid_forget()
        self.before_game_action_lst.grid_forget()
        self.button_enter.grid_forget()
        self.button_start.config(command=lambda: self.start_sell())
        self.button_start.grid(row=0, column=0)

    def start_sell(self):
        sell = Sell(self)
        sell.run()







