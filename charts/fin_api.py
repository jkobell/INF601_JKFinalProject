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

        response = requests.get(api_get, params) #get call; todo: wrap in try except; log except

        if response.status_code == 200: #status code check
            response_json = json.loads(response.text) #convert to dictionary
            return response_json
        else: 
            print(f"\n\tAPI Call failed with status code {response.status_code} at {api_get} with params: {params}") # error message if not status code 200
  