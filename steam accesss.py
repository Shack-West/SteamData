from urllib.parse import unquote, quote
import requests
from datetime import datetime 
import time
import csv
import tkinter as tk 



currency_list = {
        "AUD" : "21",
        "USD" : "1"
    }

currencies = ["AUD", "USD"]




class Item(object):
    """
    Creates an object for the item which the user
    wishes to find in the steam market/to be stored in the
    database.

    """

    def __init__(self, skin_name, currency):
        """instantiates the item"""
        self._currency = currency
        self._skin_name = skin_name
        self._base_url = f"http://steamcommunity.com/market/priceoverview/?currency={currency_list[self._currency]}&appid=730&market_hash_name="
        self._quoted = quote(self._skin_name)
        self._item_url = self._base_url + self._quoted

    def get_quoted(self):
        """
        gets the encoded the Item string
        return:
            self._quoted(string): a string representation of the UTI encoded item name
            
        """
        return self._quoted
    
    def get_url(self):
        """
        gets the url to contact the steam market with to find the item
        return:
            self._item_url(string): creates a string representation of the item url
            
        """
        return self._item_url

    def get_name(self):
        """Gets the name of the Item

        return:
            self._skin_name(string): Gets the name of the Item
        """
        return self._skin_name

    def get_currency(self):
        """Gets the currency type being used

        return:
            self._currency(string): Alphanumeric code for the currency type
        """
        return self._currency

    def change_currency(self, currency_code):
        """
        Alters the currency used in the data which is accessed
        Parameters:
            currency_code(str): The Alphanumeric code of the currency wished to be used
        return:
            self._currency(string): currency code 
            
        """
        self._currency = currency_code
        self._base_url = f"http://steamcommunity.com/market/priceoverview/?currency={currency_list[currency_code]}&appid=730&market_hash_name="
        self._item_url = self._base_url + self._quoted
        
        return self._currency

class ItemData(object):
    """Contacts the steam API and then gets the historic data about the weapon"""

    def __init__(self, weapon, weapon_url):
        """Instantiates the ItemData Object to be searched"""
        self._weapon = weapon
        self._weapon_url = weapon_url
        self._current_iteration = None
        self._time_of_iteration = None
        self._historic_mins = []
        self._historic_times = []

    def collect_data(self):
        """Sends a request to the heavens and poof; here is a dictionary of data

        return:
            self._current_iteration(dict): A dictionary of Item information
            self._time_of_iteration(str): The date and time of the current iteration
        """
        data_request = requests.get(self._weapon_url)
        self._current_iteration = data_request.json()
        self._time_of_iteration = self.get_time()
        self._historic_mins.append(self.current_min())
        self._historic_times.append(self.get_time())
        return self._time_of_iteration, self._current_iteration 

    def current_min(self):
        """Gets the Lowest price of the current iteration

        return:
            self._current_iteration['lowest_price'](str): The lowest price on the market
            
        """
        list = self._current_iteration['lowest_price'].split(" ")
        return float(list[1])

    def get_time(self):
        time = datetime.now()
        return time

    def get_times_list(self):
        return self._historic_times

    def get_min_prices(self):
        """gets a list of the historic min prices of the item

        return:
            self._historic_mins(list): A list of the historic min values
            
        """

        return self._historic_mins
        

    def get_median(self):
        """Gets the median price of the item as of the current iterations

        return:
            self._current_iteration['median_price'](str): The Current Median Price of the Item (Past Hour)
        """
        return self._current_iteration['median_price']

    def get_volume(self):
        """Finds the total volume of the item sold

        return:
            self._current_iteration['volume'](str): The current volume of the Item listed
        """
        return self._current_iteration['volume']
    









def main(): 
    root = tk.Tk()
    root.focus_set()
    root.configure(background="grey31")
    title = tk.Label(root, text="Steam Market Analysis Tool", bg="grey31")
    title.configure(font=("Comic Sans MS", 50, "bold"))
    title.pack()
    input_frame = tk.Frame(root, bg="grey31")
    input_frame.pack(ipady=20)
    auto_on = tk.StringVar(root)
    auto_on.set("Currency")
    currency_choice = tk.OptionMenu(input_frame, auto_on, "AUD", "USD")
    currency_choice.pack(side=tk.RIGHT, padx=40)
    input_entry = tk.Entry(input_frame)
    input_entry.pack(side=tk.RIGHT, ipadx=30)
    prompt = tk.Label(input_frame, text="Input Your Item: ", bg="grey31")
    prompt.configure(font=("Comic Sans MS", 15, "bold"))
    prompt.pack(side=tk.LEFT, ipadx=30)
    button_frame = tk.Frame(root, bg="grey31")
    button_frame.pack()
    sec_frame = tk.Frame(root, bg="grey31")
    sec_frame.pack()

    def get_info():
        Weapon = input_entry.get()
        Currency = auto_on.get()
        print(Weapon)
        item_info = Item(Weapon, Currency)
        global item_data
        item_data = ItemData(item_info.get_name(), item_info.get_url())
        time.sleep(3)
        st_button = tk.Button(sec_frame, text="Begin Tracking!")
        st_button.configure(font=("Comic Sans MS", 30, "bold"))
        st_button.pack(pady=50)
            
    lock_in = tk.Button(button_frame, text="Lock It In", command=get_info)
    lock_in.configure(font=("Comic Sans MS", 15, "bold"))
    lock_in.pack(ipadx=20)

    

    



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


    









