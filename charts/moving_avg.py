# INF601 - Advanced Programming in Python
# James Kobell
# Final Project
import logging
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('svg')
import numpy as np
import pandas as pd
import dateparser as dp # for parse json datetime string value
from io import StringIO
from datetime import datetime
from matplotlib.dates import DateFormatter


class MovingAvg():
    def __init__(self) -> None:
        logging.basicConfig(filename='app_log.txt', format='%(asctime)s %(message)s' ,encoding='utf-8') # log with timestamp and message.
    
    def BuildMovAvgChart(self, api_data, limit):# returns an svg image charts
        try: 
            df_raw = pd.read_json(api_data) #unsorted dataframe
            df = df_raw.sort_values(by=['date'])
        except Exception as Argument: # log if exception
            logging.exception(f"An error occured while creating a dataframe from api_data | Error: {str(Argument)}")

        begin_df_row = df.head(n=1) # parent df head
        end_df_row = df.tail(n=1) # parent df tail
        begin_df_date = pd.to_datetime(begin_df_row['date'], dayfirst=True, format='%d/%m/%Y') # date from head
        begin_df_date_str = begin_df_date.astype(str).values[0]
        begin_date_object = dp.parse(begin_df_date_str) # convert value to datetime object
        begin_date = begin_date_object.strftime("%m/%d/%Y") # format date - 01/01/2099
        end_df_date = pd.to_datetime(end_df_row['date'], dayfirst=True, format='%d/%m/%Y') # date from tail
        end_df_date_str = end_df_date.astype(str).values[0]
        end_date_object = dp.parse(end_df_date_str) # convert value to datetime object
        end_date = end_date_object.strftime("%m/%d/%Y") # format date - 01/01/2099
        close_date_dict= dict(zip(df.close, df.date))
        date_list = df['date'].to_list()
        close_arr = df['close'].to_numpy()
        symbol = df['symbol'].iat[0]
        interval = int(limit)/10
        interval_date_list = []
        for i in range(len(date_list)):
            j = i+1    
            if i == 0 or j % interval == 0:
                dt_formated = f'{date_list[i].month}-{date_list[i].day}-{date_list[i].year}' 
                interval_date_list.append(dt_formated)
            else:
                interval_date_list.append(None)
        
        """Build chart object"""
        chart_id = f"{symbol.upper()}" # value str built for chart title AND for saved png filename
        plt.ioff()
        fig = plt.figure(figsize=[9.0, 6.0], facecolor="lightblue") #new instance for each chart 
        plt.plot(close_arr)
        plt.ylabel('Moving Average')
        plt.xlabel(f'Range: {limit} trade days')
        plt.title(chart_id)
        plt.xticks(np.arange(len(interval_date_list)), interval_date_list, rotation = 90)
        plt.tight_layout() # provides padding at xticks and labels
        try: # log if exception
            plt.close()
            plt_data = StringIO()
            fig.savefig(plt_data, format='svg') # svg format for better scale/zoom image
            plt_data.seek(0)
            svg_data = plt_data.getvalue()
            return svg_data            
        except Exception as Argument: # throw if exception during savefig
            logging.exception(f"An error occured while saving chart: {chart_id} | Error: {str(Argument)}")