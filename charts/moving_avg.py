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
    logging.basicConfig(filename='app_log.txt', format='%(asctime)s %(message)s' ,encoding='utf-8') # log with timestamp and message.
    #ticker = 'TSLA' # todo: make interactive with input control
    #data_filename = (f"app_data/{ticker}.csv")
    raw = '[{"open":23.07,"high":23.54,"low":22.95,"close":23.46,"volume":411100.0,"adj_high":23.54,"adj_low":22.95,"adj_close":23.46,"adj_open":23.07,"adj_volume":411134.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-25T00:00:00+0000"},{"open":22.79,"high":23.32,"low":22.62,"close":23.08,"volume":820100.0,"adj_high":23.32,"adj_low":22.62,"adj_close":23.08,"adj_open":22.79,"adj_volume":820087.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-23T00:00:00+0000"},{"open":22.21,"high":23.11,"low":22.12,"close":22.99,"volume":1023900.0,"adj_high":23.105,"adj_low":22.12,"adj_close":22.99,"adj_open":22.21,"adj_volume":1023909.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-22T00:00:00+0000"},{"open":21.67,"high":22.1425,"low":21.65,"close":22.1,"volume":898122.0,"adj_high":22.1425,"adj_low":21.65,"adj_close":22.1,"adj_open":21.67,"adj_volume":898148.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-21T00:00:00+0000"},{"open":22.5,"high":22.55,"low":21.7,"close":21.94,"volume":661900.0,"adj_high":22.55,"adj_low":21.7,"adj_close":21.94,"adj_open":22.5,"adj_volume":661925.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-18T00:00:00+0000"},{"open":21.74,"high":22.12,"low":21.41,"close":22.07,"volume":605200.0,"adj_high":22.12,"adj_low":21.41,"adj_close":22.07,"adj_open":21.74,"adj_volume":605196.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-17T00:00:00+0000"},{"open":22.79,"high":23.0,"low":22.12,"close":22.21,"volume":641469.0,"adj_high":23.0,"adj_low":22.12,"adj_close":22.21,"adj_open":22.79,"adj_volume":746729.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-16T00:00:00+0000"},{"open":22.74,"high":23.26,"low":22.6,"close":23.18,"volume":2038200.0,"adj_high":23.26,"adj_low":22.6,"adj_close":23.18,"adj_open":22.74,"adj_volume":2038161.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-15T00:00:00+0000"},{"open":22.7,"high":22.93,"low":22.18,"close":22.19,"volume":1634000.0,"adj_high":22.93,"adj_low":22.18,"adj_close":22.19,"adj_open":22.7,"adj_volume":1634019.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-14T00:00:00+0000"},{"open":22.86,"high":23.18,"low":22.35,"close":23.07,"volume":2005700.0,"adj_high":23.18,"adj_low":22.35,"adj_close":23.07,"adj_open":22.86,"adj_volume":2005657.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-11T00:00:00+0000"},{"open":21.84,"high":22.25,"low":21.73,"close":22.22,"volume":1475941.0,"adj_high":22.25,"adj_low":21.73,"adj_close":22.22,"adj_open":21.84,"adj_volume":1576821.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-10T00:00:00+0000"},{"open":20.42,"high":20.86,"low":20.24,"close":20.64,"volume":1271000.0,"adj_high":20.86,"adj_low":20.235,"adj_close":20.64,"adj_open":20.42,"adj_volume":1270962.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-09T00:00:00+0000"},{"open":20.92,"high":21.25,"low":20.36,"close":20.71,"volume":999300.0,"adj_high":21.25,"adj_low":20.355,"adj_close":20.71,"adj_open":20.92,"adj_volume":999313.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-08T00:00:00+0000"},{"open":20.51,"high":20.84,"low":19.99,"close":20.83,"volume":1876000.0,"adj_high":20.835,"adj_low":19.99,"adj_close":20.83,"adj_open":20.51,"adj_volume":1876058.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-07T00:00:00+0000"},{"open":20.58,"high":20.65,"low":19.57,"close":20.12,"volume":1545700.0,"adj_high":20.65,"adj_low":19.57,"adj_close":20.12,"adj_open":20.58,"adj_volume":1545979.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-04T00:00:00+0000"},{"open":20.0,"high":20.3,"low":19.55,"close":20.07,"volume":1272600.0,"adj_high":20.3,"adj_low":19.55,"adj_close":20.07,"adj_open":20.0,"adj_volume":1272628.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-03T00:00:00+0000"},{"open":21.23,"high":21.4,"low":20.26,"close":20.31,"volume":1014800.0,"adj_high":21.4,"adj_low":20.255,"adj_close":20.31,"adj_open":21.23,"adj_volume":1014775.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-02T00:00:00+0000"},{"open":21.74,"high":21.8,"low":21.21,"close":21.36,"volume":1345800.0,"adj_high":21.795,"adj_low":21.21,"adj_close":21.36,"adj_open":21.74,"adj_volume":1345787.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-11-01T00:00:00+0000"},{"open":20.99,"high":21.41,"low":20.91,"close":21.26,"volume":1161400.0,"adj_high":21.41,"adj_low":20.91,"adj_close":21.26,"adj_open":20.99,"adj_volume":1161353.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-31T00:00:00+0000"},{"open":20.33,"high":21.19,"low":20.26,"close":21.18,"volume":938500.0,"adj_high":21.19,"adj_low":20.26,"adj_close":21.18,"adj_open":20.33,"adj_volume":938469.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-28T00:00:00+0000"},{"open":20.68,"high":21.12,"low":20.36,"close":20.45,"volume":1635100.0,"adj_high":21.12,"adj_low":20.36,"adj_close":20.45,"adj_open":20.68,"adj_volume":1635070.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-27T00:00:00+0000"},{"open":20.31,"high":21.2,"low":19.45,"close":20.57,"volume":2781400.0,"adj_high":21.2,"adj_low":19.45,"adj_close":20.57,"adj_open":20.31,"adj_volume":2781441.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-26T00:00:00+0000"},{"open":19.45,"high":20.51,"low":19.45,"close":20.3,"volume":2518700.0,"adj_high":20.51,"adj_low":19.45,"adj_close":20.3,"adj_open":19.45,"adj_volume":2518857.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-25T00:00:00+0000"},{"open":19.36,"high":19.49,"low":18.66,"close":19.38,"volume":1491083.0,"adj_high":19.49,"adj_low":18.66,"adj_close":19.38,"adj_open":19.36,"adj_volume":1491186.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-24T00:00:00+0000"},{"open":18.87,"high":19.38,"low":18.77,"close":19.35,"volume":1643900.0,"adj_high":19.375,"adj_low":18.77,"adj_close":19.35,"adj_open":18.87,"adj_volume":1643994.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-21T00:00:00+0000"},{"open":19.12,"high":19.56,"low":18.82,"close":18.96,"volume":1493800.0,"adj_high":19.56,"adj_low":18.82,"adj_close":18.96,"adj_open":19.12,"adj_volume":1493823.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-20T00:00:00+0000"},{"open":19.3,"high":19.55,"low":18.77,"close":19.03,"volume":1317400.0,"adj_high":19.55,"adj_low":18.77,"adj_close":19.03,"adj_open":19.3,"adj_volume":1317429.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-19T00:00:00+0000"},{"open":20.21,"high":20.5,"low":19.45,"close":19.6,"volume":1302700.0,"adj_high":20.5,"adj_low":19.455,"adj_close":19.6,"adj_open":20.21,"adj_volume":1302720.0,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-18T00:00:00+0000"},{"open":19.2,"high":19.79,"low":19.13,"close":19.56,"volume":2024600.0,"adj_high":null,"adj_low":null,"adj_close":19.56,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-17T00:00:00+0000"},{"open":19.23,"high":19.38,"low":18.57,"close":18.64,"volume":1106600.0,"adj_high":null,"adj_low":null,"adj_close":18.64,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-14T00:00:00+0000"},{"open":18.29,"high":19.41,"low":18.06,"close":19.05,"volume":1823502.0,"adj_high":null,"adj_low":null,"adj_close":19.05,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-13T00:00:00+0000"},{"open":18.73,"high":18.97,"low":18.4,"close":18.78,"volume":1732500.0,"adj_high":null,"adj_low":null,"adj_close":18.78,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-12T00:00:00+0000"},{"open":18.8,"high":19.09,"low":18.2,"close":18.73,"volume":1660100.0,"adj_high":null,"adj_low":null,"adj_close":18.73,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-11T00:00:00+0000"},{"open":19.33,"high":19.41,"low":18.81,"close":18.92,"volume":1365000.0,"adj_high":null,"adj_low":null,"adj_close":18.92,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-10T00:00:00+0000"},{"open":19.76,"high":19.95,"low":18.74,"close":19.32,"volume":2047500.0,"adj_high":null,"adj_low":null,"adj_close":19.32,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-07T00:00:00+0000"},{"open":20.29,"high":20.51,"low":20.03,"close":20.2,"volume":1619469.0,"adj_high":null,"adj_low":null,"adj_close":20.2,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-06T00:00:00+0000"},{"open":20.2,"high":20.67,"low":20.0,"close":20.5,"volume":1503200.0,"adj_high":null,"adj_low":null,"adj_close":20.5,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-05T00:00:00+0000"},{"open":20.73,"high":21.07,"low":20.56,"close":20.8,"volume":2537900.0,"adj_high":null,"adj_low":null,"adj_close":20.8,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-04T00:00:00+0000"},{"open":19.37,"high":20.26,"low":19.19,"close":20.18,"volume":2555400.0,"adj_high":null,"adj_low":null,"adj_close":20.18,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-10-03T00:00:00+0000"},{"open":19.39,"high":19.87,"low":18.98,"close":19.01,"volume":1686800.0,"adj_high":null,"adj_low":null,"adj_close":19.01,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-30T00:00:00+0000"},{"open":20.05,"high":20.28,"low":19.015,"close":19.41,"volume":2502607.0,"adj_high":null,"adj_low":null,"adj_close":19.41,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-29T00:00:00+0000"},{"open":20.53,"high":20.815,"low":20.37,"close":20.53,"volume":1975806.0,"adj_high":null,"adj_low":null,"adj_close":20.53,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-28T00:00:00+0000"},{"open":20.98,"high":21.28,"low":20.315,"close":20.47,"volume":1498942.0,"adj_high":null,"adj_low":null,"adj_close":20.47,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-27T00:00:00+0000"},{"open":20.86,"high":21.35,"low":20.52,"close":20.67,"volume":1675600.0,"adj_high":null,"adj_low":null,"adj_close":20.67,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-26T00:00:00+0000"},{"open":21.21,"high":21.42,"low":20.62,"close":20.85,"volume":2208500.0,"adj_high":null,"adj_low":null,"adj_close":20.85,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-23T00:00:00+0000"},{"open":21.78,"high":21.92,"low":21.34,"close":21.63,"volume":2581689.0,"adj_high":null,"adj_low":null,"adj_close":21.63,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-22T00:00:00+0000"},{"open":22.33,"high":23.04,"low":21.96,"close":21.99,"volume":2693302.0,"adj_high":null,"adj_low":null,"adj_close":21.99,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-21T00:00:00+0000"},{"open":22.81,"high":22.96,"low":21.87,"close":22.22,"volume":3231121.0,"adj_high":null,"adj_low":null,"adj_close":22.22,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-20T00:00:00+0000"},{"open":22.51,"high":23.13,"low":22.19,"close":23.13,"volume":4946198.0,"adj_high":null,"adj_low":null,"adj_close":23.13,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-19T00:00:00+0000"},{"open":23.12,"high":23.53,"low":21.64,"close":23.2,"volume":13555900.0,"adj_high":null,"adj_low":null,"adj_close":23.2,"adj_open":null,"adj_volume":null,"split_factor":1.0,"dividend":0.0,"symbol":"NCR","exchange":"XNYS","date":"2022-09-16T00:00:00+0000"}]'

    def BuildMovAvgChart(self, api_data, limit):
        #limit = '50'
        try: # log if exception
            #df_raw = pd.read_json(raw)
            df_raw = pd.read_json(self.raw)
            #df_raw = pd.read_json(api_data)
            df = df_raw.sort_values(by=['date'])
        except Exception as Argument:
            logging.exception(f"An error occured while creating a dataframe from {api_data} | Error: {str(Argument)}")

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
                #interval_date_list.append(date_list[i])
                interval_date_list.append(dt_formated)
            else:
                interval_date_list.append(None)



        #tick_date_intervals =[datetime(2012,1,i+3) for i in range(date_list)]
        #tick_date_intervals = [pd.to_datetime(date, format='%Y-%m-%d').date() for date in date_list]

        #aar = np.array(close_date_dict['close'])
        #close_average_df = pd.DataFrame(gg) # new df for plotting
        #chart_id = f"{symbol} - {begin_year_df_year}" # value str built for chart title AND for png filename
        chart_id = f"{symbol.upper()}" # value str built for chart title AND for png filename
        plt.ioff()
        fig = plt.figure(figsize=[9.0, 6.0], facecolor="lightblue") #new instance for each chart 
        plt.plot(close_arr)
        plt.ylabel('Moving Average')
        plt.xlabel(f'Range: {limit} trade days')
        #plt.xlabel(f'Range: 50 trading days')
        plt.title(chart_id)
        plt.xticks(np.arange(len(interval_date_list)), interval_date_list, rotation = 90)
        plt.tight_layout() # provides padding at xticks and labels
        try: # log if exception
            #plt.savefig(f'eod_charts/{chart_id}.png', facecolor="#cfd9e4") # create charts as png files
            plt.close()
            plt_data = StringIO()
            fig.savefig(plt_data, format='svg')
            plt_data.seek(0)
            svg_data = plt_data.getvalue()
            #print(svg_data)
            return svg_data            
        except Exception as Argument: # throw if exception during savefig
            logging.exception(f"An error occured while saving chart: {chart_id} | Error: {str(Argument)}")
        #plt.show() # uncomment for degugging
    
    








""" begin_year_df_date_int32 = begin_df_date.dt.year.astype(int).values[0] # date to int - used for incrementing 
begin_df_year = str(begin_year_df_date_int32) #int32 to string - used for f" interpolation
end_df_date_int32 = end_df_date.dt.year.astype(int).values[0] # date to int - used for incrementing
end_df_year = str(end_df_date_int32) #int32 to string - used for f" interpolation
years_df_range = end_df_date_int32 - begin_year_df_date_int32 + 1 # parent df year range
for i in range(years_df_range): #iterate parent df. append each child/year df to years list
    if begin_df_year:
        df_year = df[(df['date'] >= f"{begin_df_year}-01-01") & (df['date'] <= f"{begin_df_year}-12-31")]
        begin_year_df_date_int32 += 1
        begin_df_year = str(begin_year_df_date_int32)
        df_years.append(df_year)
for item in df_years: # iterate each year df. query year and month for each
    df_item = pd.DataFrame(item) # cast as a DataFrame
    begin_year_df_row = df_item.head(n=1)
    end_year_df_row = df_item.tail(n=1)    
    begin_year_df_date = pd.to_datetime(begin_year_df_row['date'])
    end_year_df_date = pd.to_datetime(end_year_df_row['date'])
    begin_year_df_date_int32 = begin_year_df_date.dt.year.astype(int).values[0]
    begin_year_df_year = str(begin_year_df_date_int32) #int32 to string
    begin_month_df_date_int32 = begin_year_df_date.dt.month.astype(int).values[0]
    begin_month_df_date = str(begin_month_df_date_int32) #int32 to string
    end_month_df_date_int32 = end_year_df_date.dt.month.astype(int).values[0]
    end_month_df_date = str(end_month_df_date_int32) #int32 to string
    months_df_range = end_month_df_date_int32 - begin_month_df_date_int32 + 1
    df_months = [] # declare months df list
    for i in range(months_df_range): # iterate available months in year. append each month df to df_months list
        if begin_month_df_date:
            if len(begin_month_df_date) == 1: # if month digits is less than 2 prepend a 0
                begin_month_df_date = f"0{begin_month_df_date}"

            df_month = df_item[(df_item['date'] >= f"{begin_year_df_year}-{begin_month_df_date}-01") & (df_item['date'] <= f"{begin_year_df_year}-{begin_month_df_date}-30")]

            begin_month_df_date_int32 += 1
            begin_month_df_date = str(begin_month_df_date_int32)
            df_months.append(df_month)
    
    for month_item in df_months: # iterate df_months list
        df_month_item = pd.DataFrame(month_item) # cast as a DataFrame
        month_begin_df_row = df_month_item.head(n=1)
        month_end_df_row = df_month_item.tail(n=1)
        month_begin_df_date = pd.to_datetime(month_begin_df_row['date'])
        month_end_df_date = pd.to_datetime(month_end_df_row['date'])
        month_begin_df_date_str = month_begin_df_date.astype(str).values[0]
        month_end_df_date_str = month_end_df_date.astype(str).values[0]

        begin_month_df_date_int32 = month_begin_df_date.dt.month.astype(int).values[0]
        begin_month_df_date = str(begin_month_df_date_int32) #int32 to string
        end_month_df_date_int32 = month_end_df_date.dt.month.astype(int).values[0]
        end_month_df_date = str(end_month_df_date_int32) #int32 to string


        begin_day_df_date_int32 = month_begin_df_date.dt.day.astype(int).values[0]
        begin_day_df_date = str(begin_day_df_date_int32) #int32 to string
        end_day_df_date_int32 = month_end_df_date.dt.day.astype(int).values[0]
        end_day_df_date = str(end_day_df_date_int32) #int32 to string
        days_df_range = end_day_df_date_int32 - begin_day_df_date_int32 + 1

        df_days = [] # declare months df list
        for i in range(days_df_range):
            if begin_day_df_date:
                if len(begin_day_df_date) == 1: # if month digits is less than 2 prepend a 0
                    begin_day_df_date = f"0{begin_day_df_date}"

                df_day = df_month_item[(df_month_item['date'] >= f"{begin_year_df_year}-{begin_month_df_date}-{begin_day_df_date}") & (df_month_item['date'] <= f"{begin_year_df_year}-{begin_month_df_date}-{end_day_df_date}")]

                begin_day_df_date_int32 += 1
                begin_day_df_date = str(begin_day_df_date_int32)
                df_days.append(df_day)

        close_average = []
        days_xticks_labels = []
        for day_item in df_days: # iterate df_days list
            df_day_item = pd.DataFrame(day_item) # cast as a DataFrame
            day_begin_df_row = df_day_item.head(n=1)
           # day_end_df_row = df_day_item.tail(n=1)
            day_begin_df_date = pd.to_datetime(day_begin_df_row['date'])
           # day_end_df_date = pd.to_datetime(day_end_df_row['date'])
            day_begin_df_date_str = day_begin_df_date.astype(str).values[0]
            #day_end_df_date_str = day_end_df_date.astype(str).values[0]
            #change below to days
            #day_xtick_label = f"{month_begin_df_date_str}\n- {month_end_df_date_str}" # build xticks label
            day_xtick_label = f"{day_begin_df_date_str}" # build xticks label
            day_item_count = len(df_day_item) # for x-axis datapoints formatting
            day_close_price = df_day_item['close']
            if ((day_item_count >= 1)): # check for values            
                #month_close_average = month_close_prices_sum / month_item_count
                close_average.append(day_close_price)
                days_xticks_labels.append(day_xtick_label)# provide label conditionally. only if moving average 
        gg = close_average[1]
        close_average_df = pd.DataFrame(gg) # new df for plotting
        #chart_id = f"{symbol} - {begin_year_df_year}" # value str built for chart title AND for png filename
        chart_id = f"NCR - Test Month" # value str built for chart title AND for png filename
        plt.figure() #new instance for each chart 
        plt.plot(close_average_df)
        plt.ylabel('Moving Average')
        plt.title(chart_id)
        plt.xticks(np.arange(len(close_average)), days_xticks_labels, rotation = 70)
        plt.tight_layout() # provides padding at xticks and labels
        try: # log if exception
            plt.savefig(f"eod_charts/{chart_id}.png", facecolor = "#cfd9e4") # create charts as png files
        except Exception as Argument: # throw if exception during savefig
            logging.exception(f"An error occured while saving chart: {chart_id} | Error: {str(Argument)}")
        plt.show() # uncomment for degugging """

                   
    