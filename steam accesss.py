from urllib.parse import unquote, quote
import requests
from datetime import datetime 
import time
import csv
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


currency_list = {
        "AUD" : "21",
        "USD" : "1",
        "GBP" : "2",
    }

currencies = ["AUD", "USD"]


class dataCollector(object):

    def __init__(self):
        self._root = tk.Tk()
        self._root.focus_set()
        self._root.configure(background="grey31")
        self._title = tk.Label(self._root, text="Steam Market Analysis Tool", bg="grey31")
        self._title.configure(font=("Comic Sans MS", 50, "bold"))
        self._title.pack()
        self._input_frame = tk.Frame(self._root, bg="grey31")
        self._input_frame.pack(ipady=20)
        self._auto_on = tk.StringVar(self._root)
        self._auto_on.set("Currency")
        self._currency_choice = tk.OptionMenu(self._input_frame, self._auto_on, "AUD", "USD")
        self._currency_choice.pack(side=tk.RIGHT, padx=40)
        self._input_entry = tk.Entry(self._input_frame)
        self._input_entry.pack(side=tk.RIGHT, ipadx=30)
        self._prompt = tk.Label(self._input_frame, text="Input Your Item: ", bg="grey31")
        self._prompt.configure(font=("Comic Sans MS", 15, "bold"))
        self._prompt.pack(side=tk.LEFT, ipadx=30)
        self._button_frame = tk.Frame(self._root, bg="grey31")
        self._button_frame.pack()
        self._sec_frame = tk.Frame(self._root, bg="grey31")
        self._sec_frame.pack()
        self._lock_in = tk.Button(self._button_frame, text="Lock It In", command=self.get_nc)
        self._lock_in.configure(font=("Comic Sans MS", 15, "bold"))
        self._lock_in.pack(ipadx=20)
        self._base_url = None
        self._skin_name = None
        self._currency_name = None
        self._url = None
        self._new_data = None
        self._min_value = None
        self._fig = plt.figure()
        self._sub = self._fig.add_subplot(1,1,1)
        self._x = []
        self._y = []

    def get_nc(self):
        self._skin_name = self._input_entry.get().strip()
        self._currency_name = self._auto_on.get()
        self._base_url = f"http://steamcommunity.com/market/priceoverview/?currency={currency_list[self._currency_name]}&appid=730&market_hash_name="
        self._url = self._base_url + quote(self._skin_name)
        self._start_button = tk.Button(self._sec_frame, text="Begin Tracking!", command=self.create_plot)
        self._start_button.configure(font=("Comic Sans MS", 30, "bold"))
        self._start_button.pack(pady=30)
        

    def collect_data(self):
        data_request = requests.get(self._url)
        self._new_data = data_request.json()
        

    def get_cur_min(self):
        min_value = ''
        new_data = self._new_data['lowest_price']
        for i in new_data:
            if i.isdigit() or i == ".":
                min_value += i
        return float(min_value)
        
        


    def _animate(self, i):
        self.collect_data()
        cm = self.get_cur_min()
        self._y.append(cm)
        self._x.append(len(self._y))
        self._sub.clear()
        self._sub.plot(self._x,self._y)
        plt.xlabel("Relative Time")
        plt.ylabel(f"Price ({self._currency_name})")
        plt.title(f"{self._skin_name}")
        
        

    def create_plot(self):
        animation = FuncAnimation(self._fig, self._animate, interval=15000)
        plt.show()

def main():
    m = dataCollector()


    



if __name__ == "__main__":
    main()



##gun = Item("Operation Breakout Weapon Case", "AUD")
##gunData = ItemData(gun.get_name(), gun.get_url())
##
##
##    
##fieldnames = ["Datetime", "Current Min Price"]
##
##with open("currentdata.csv", 'w') as csv_file:
##    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
##    csv_writer.writeheader()
##
##
##while True:
##    gunData.collect_data()
##    with open("currentdata.csv", "a") as csv_file:
##        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
##
##
##        datetime = gunData.get_time()
##        current_min = gunData.current_min()
##        
##        info = {
##            "Datetime": datetime,
##            "Current Min Price": current_min
##        }
##
##
##        csv_writer.writerow(info)
##        print(datetime, current_min)
##        
##        
##    time.sleep(10)
##
##        


    









