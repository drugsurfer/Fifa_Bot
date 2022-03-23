from tkinter import *
import data


class Filter:
    def __init__(self, obj):
        self.root = obj.root
        self.parent_object = obj
        if self.parent_object.data.type_buy_object == 'CP':
            self.app_list(data.QualityList, obj.QualityList)
            self.app_list(data.Position, obj.Position)
            self.app_list(data.Nationality, obj.Nationality)
            self.app_list(data.Club, obj.Club)
            self.app_list(data.Rarity, obj.Rarity)
            self.app_list(data.ChemistryStyle, obj.ChemistryStyle)
            self.app_list(data.League, obj.League)
            self.draw_widgets_for_cp()
        elif self.parent_object.data.type_buy_object == 'CPos':
            self.app_list(data.QualityList_Pos_Ch, obj.QualityList)
            self.app_list(data.Position_Pos_Ch, obj.Position)
            self.draw_widgets_for_cpos()
        else:
            self.app_list(data.QualityList_Pos_Ch, obj.QualityList)
            self.app_list(data.ChemistryStyle_Ch_S, obj.ChemistryStyle)
            self.draw_widgets_for_ts()

    def draw_widgets_for_cp(self):
        self.parent_object.QualityList.grid(row=0, column=0)
        self.parent_object.Position.grid(row=0, column=1)
        self.parent_object.Nationality.grid(row=0, column=2)
        self.parent_object.Club.grid(row=1, column=0)
        self.parent_object.Rarity.grid(row=1, column=1)
        self.parent_object.ChemistryStyle.grid(row=1, column=2)
        self.parent_object.League.grid(row=2, column=1)
        self.parent_object.min.grid(row=3, column=0)
        self.parent_object.max.grid(row=3, column=1)
        self.parent_object.Name.grid(row=3, column=2)
        if self.parent_object.data.type_bid == 'Bid':
            self.parent_object.checkStartMax.grid(row=4, column=2)
            self.parent_object.checkStartMin.grid(row=5, column=2)
        self.parent_object.button_reset.grid(row=0, column=3)
        self.parent_object.button_search.grid(row=1, column=3)

    def draw_widgets_for_cpos(self):
        self.parent_object.QualityList.grid(row=0, column=0)
        self.parent_object.Position.grid(row=0, column=1)
        self.parent_object.min.grid(row=1, column=0)
        self.parent_object.max.grid(row=1, column=1)
        self.parent_object.button_reset.grid(row=1, column=2)
        self.parent_object.button_search.grid(row=0, column=2)
        if self.parent_object.data.type_bid == 'Bid':
            self.parent_object.checkStartMax.grid(row=2, column=0)
            self.parent_object.checkStartMin.grid(row=3, column=0)

    def draw_widgets_for_ts(self):
        self.parent_object.QualityList.grid(row=0, column=0)
        self.parent_object.ChemistryStyle.grid(row=0, column=1)
        self.parent_object.min.grid(row=1, column=0)
        self.parent_object.max.grid(row=1, column=1)
        self.parent_object.button_reset.grid(row=1, column=2)
        self.parent_object.button_search.grid(row=0, column=2)
        if self.parent_object.data.type_bid == 'Bid':
            self.parent_object.checkStartMax.grid(row=2, column=0)
            self.parent_object.checkStartMin.grid(row=3, column=0)

    def app_list(self, dct, lst):
        for index in sorted(dct.keys()):
            lst.insert(END, dct[index][0])

    def on_time_widgets(self):
        self.parent_object.count_good_bets.grid(row=0, column=0)
        self.parent_object.count_bad_bets.grid(row=1, column=0)
        self.parent_object.gap_count.grid(row=0, column=1)
        self.parent_object.bad_search_count.grid(row=1, column=1)
        self.parent_object.time_to_timeout.grid(row=0, column=2)
        self.parent_object.time_timeout.grid(row=1, column=2)
        self.parent_object.time_to_filters.grid(row=0, column=3)
        self.parent_object.time_to_transfer.grid(row=1, column=3)
        if self.parent_object.data.type_bid == 'Bid' and self.parent_object.data.check == 0:
            self.parent_object.max_user_Bid.grid(row=2, column=2)
        self.parent_object.button_enter.grid(row=1, column=4)

    def set_filters(self):
        res_data = self.parent_object.data
        for key in res_data.inputData.keys():
            if key in ['Name', 'MaxBid', 'MinBid', 'MaxBuy', 'MinBuy']:
                data_ = res_data.inputData[key]
                self.parent_object.device.inputForm(data_[1],
                                                    data_[0])
            else:
                data_ = res_data.inputData[key]
                if not (data_[1] == data_[0] == ''):
                    self.parent_object.device.clickHiddenButton(data_[1],
                                                                data_[0])

    def input_data(self):
        res_data = self.parent_object.data
        if self.parent_object.data.type_buy_object == 'CP':
            res_data.add_data('Name', self.parent_object.Name.get())
            res_data.add_data('QualityList', self.parent_object.QualityList.curselection())
            res_data.add_data('Position', self.parent_object.Position.curselection())
            res_data.add_data('Nationality', self.parent_object.Nationality.curselection())
            res_data.add_data('Club', self.parent_object.Club.curselection())
            res_data.add_data('Rarity', self.parent_object.Rarity.curselection())
            res_data.add_data('ChemistryStyle', self.parent_object.ChemistryStyle.curselection())
            res_data.add_data('League', self.parent_object.League.curselection())
            if self.parent_object.data.type_bid == 'Bid':
                res_data.add_data('MaxBid', self.parent_object.max.get())
                res_data.add_data('MinBid', self.parent_object.min.get())
                res_data.check = self.parent_object.check
            else:
                res_data.add_data('MaxBuy', self.parent_object.max.get())
                res_data.add_data('MinBuy', self.parent_object.min.get())
            self.off_widgets_for_cp()
        elif self.parent_object.data.type_buy_object == 'CPos':
            res_data.add_data('QualityList_Pos_Ch', self.parent_object.QualityList.curselection())
            res_data.add_data('Position_Pos_Ch', self.parent_object.Position.curselection())
            if self.parent_object.data.type_bid == 'Bid':
                res_data.add_data('MaxBid', self.parent_object.max.get())
                res_data.add_data('MinBid', self.parent_object.min.get())
                res_data.check = self.parent_object.check
            else:
                res_data.add_data('MaxBuy', self.parent_object.max.get())
                res_data.add_data('MinBuy', self.parent_object.min.get())
            self.off_widgets_for_cpos()
        else:
            res_data.add_data('QualityList_Pos_Ch', self.parent_object.QualityList.curselection())
            res_data.add_data('ChemistryStyle_Ch_S', self.parent_object.ChemistryStyle.curselection())
            if self.parent_object.data.type_bid == 'Bid':
                res_data.add_data('MaxBid', self.parent_object.max.get())
                res_data.add_data('MinBid', self.parent_object.min.get())
                res_data.check = self.parent_object.check
            else:
                res_data.add_data('MaxBuy', self.parent_object.max.get())
                res_data.add_data('MinBuy', self.parent_object.min.get())
            self.off_widgets_for_ts()
        self.on_time_widgets()

    def off_widgets_for_cp(self):
        self.parent_object.QualityList.grid_forget()
        self.parent_object.Position.grid_forget()
        self.parent_object.Nationality.grid_forget()
        self.parent_object.Club.grid_forget()
        self.parent_object.Rarity.grid_forget()
        self.parent_object.ChemistryStyle.grid_forget()
        self.parent_object.League.grid_forget()
        self.parent_object.min.grid_forget()
        self.parent_object.max.grid_forget()
        self.parent_object.Name.grid_forget()
        if self.parent_object.data.type_bid == 'Bid':
            self.parent_object.checkStartMax.grid_forget()
            self.parent_object.checkStartMin.grid_forget()
        self.parent_object.button_reset.grid_forget()
        self.parent_object.button_search.grid_forget()

    def off_widgets_for_cpos(self):
        self.parent_object.QualityList.grid_forget()
        self.parent_object.Position.grid_forget()
        self.parent_object.min.grid_forget()
        self.parent_object.max.grid_forget()
        self.parent_object.button_reset.grid_forget()
        self.parent_object.button_search.grid_forget()
        if self.parent_object.data.type_bid == 'Bid':
            self.parent_object.checkStartMax.grid_forget()
            self.parent_object.checkStartMin.grid_forget()

    def off_widgets_for_ts(self):
        self.parent_object.min.grid_forget()
        self.parent_object.max.grid_forget()
        self.parent_object.QualityList.grid_forget()
        self.parent_object.ChemistryStyle.grid_forget()
        self.parent_object.button_reset.grid_forget()
        self.parent_object.button_search.grid_forget()
        if self.parent_object.data.type_bid == 'Bid':
            self.parent_object.checkStartMax.grid_forget()
            self.parent_object.checkStartMin.grid_forget()


