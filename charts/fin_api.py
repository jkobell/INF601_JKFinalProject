# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
import requests
import json
import numpy as np # import numpy
import matplotlib.pyplot as plt # import matplotlib.pyplot
import dateparser as dp # for parse json datetime string value
from fin_ticker import settings 

class FinApi():
    #access_key = "place key here" # DO NOT show in commits; todo: get from file
    api_base_url = 'http://api.marketstack.com/v1'

    def __init__(self) -> None:
        self.access_key = settings.API_ACCESS_KEY

    def getEod(self, eod_date, symbol, is_latest):
        print(eod_date, symbol, is_latest)
        #pass
        path = 'eod'
        api_get = ''
        params = {
            "access_key" : self.access_key,
            "symbols" : symbol
            }
       
        if is_latest:
            api_get = f'{self.api_base_url}/{path}/{"latest"}'
        else:
           api_get = f'{self.api_base_url}/{path}/{eod_date}' 
        #print(api_get)
        response = requests.get(api_get, params) #get call; todo: wrap in try except; log except

        if response.status_code == 200: #status code check
            response_json = json.loads(response.text) #convert to dictionary
            return response_json
        else: 
            print(f"\n\tAPI Call failed with status code {response.status_code} at {api_get} with params: {params}") # error message if not status code 200
  
        #jsonstr = '{"pagination":{"limit":100,"offset":0,"count":1,"total":1},"data":[{"open":22.21,"high":23.11,"low":22.12,"close":22.99,"volume":1023900.0,"adj_high":23.105,"adj_low":22.12,"adj_close":22.99,"adj_open":22.21,"adj_volume":1023909.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-22T00:00:00+0000"}]}'
        #response_json = json.loads(jsonstr) #convert to dictionary
        #return response_json
class EodData(object):

    def __init__(self, open, high, low, close, volume, adj_high, adj_low, adj_close, adj_open, adj_volume, split_factor, dividend, symbol, exchange, date):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adj_high = adj_high
        self.adj_low = adj_low
        self.adj_close = adj_close
        self.adj_open = adj_open
        self.adj_volume = adj_volume
        self.split_factor = split_factor
        self.dividend = dividend
        self.symbol = symbol
        self.exchange = exchange
        self.date = date
        
    
    """ def __iter__(self):
        return iter(self.pairs)

    def __subclasses__(self: Self) -> list[Self]:
        pass

    def __dict__(self):
        return self.__iter__ """

    """ def bobb(self):
        return self.__dict__.items() """

    def __repr__(self):
        self.__setattr__('open', self.open)
        self.__setattr__('high', self.high)
        return super().__repr__()

    """ def __str__(self):
        return str(self.open) """
        #, self.high, self.low, self.close

    """ def to_json(self):
        return self.__str__() """

    @staticmethod
    def from_json(json_obj):
      return EodData(json_obj['open'], json_obj['high'], json_obj['low'], json_obj['close'], json_obj['volume'],
                    json_obj['adj_high'], json_obj['adj_low'], json_obj['adj_close'], json_obj['adj_open'], json_obj['adj_volume'],
                    json_obj['split_factor'], json_obj['dividend'], json_obj['symbol'], json_obj['exchange'], json_obj['date'])
                     
                     
