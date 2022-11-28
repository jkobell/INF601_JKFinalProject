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
    api_base_url = 'http://api.marketstack.com/v1'

    def __init__(self) -> None:
        self.access_key = settings.API_ACCESS_KEY #!!! DO NOT COMMIT !!!

    def getEod(self, eod_date, symbol, is_latest):
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

        """ response = requests.get(api_get, params) #get call; todo: wrap in try except; log except

        if response.status_code == 200: #status code check
            response_json = json.loads(response.text) #convert to dictionary
            return response_json
        else: 
            print(f"\n\tAPI Call failed with status code {response.status_code} at {api_get} with params: {params}") # error message if not status code 200
   """
        jsonstr = '{"pagination":{"limit":100,"offset":0,"count":1,"total":1},"data":[{"open":22.21,"high":23.11,"low":22.12,"close":22.99,"volume":1023900.0,"adj_high":23.105,"adj_low":22.12,"adj_close":22.99,"adj_open":22.21,"adj_volume":1023909.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-22T00:00:00+0000"}]}'
        response_json = json.loads(jsonstr) #convert to dictionary
        return response_json
    
    def getEodLimit(self, limit, symbol):
        path = 'eod'
        api_get = ''
        params = {
            "access_key" : self.access_key,
            "symbols" : symbol,
            "limit" : limit
            }
        
        api_get = f'{self.api_base_url}/{path}'

        response = requests.get(api_get, params) #get call; todo: wrap in try except; log except

        if response.status_code == 200: #status code check
            response_json = json.loads(response.text) #convert to dictionary
            return response_json
        else: 
            print(f"\n\tAPI Call failed with status code {response.status_code} at {api_get} with params: {params}") # error message if not status code 200
  





