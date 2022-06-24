from tkinter.messagebox import *
from datetime import datetime
from pathlib import Path
import yfinance as yf
import tkinter
import csv
import os

root = tkinter.Tk()
root.withdraw()

home = str(Path.home())

location = 'C:\\ProgramData\\StockHC\\'
database_loca = f'{home}\\StockHC\\database\\'
temp_loca = f'{home}\\StockHC\\temp\\'
days_loca = f'{home}\\StockHC\\day_lists\\'

'''if os.path.isfile(location):
    os.mkdir(location)
if os.path.isfile(database_loca):
    os.mkdir(database_loca)'''

print(days_loca)

'''data = yf.download(
    # tickers list or string as well
    tickers="SPY AAPL MSFT",

    # use "period" instead of start/end
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # (optional, default is '1mo')
    period="ytd",

    # fetch data by interval (including intraday if period < 60 days)
    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # (optional, default is '1d')
    interval="1m",

    # group by ticker (to access via data['SPY'])
    # (optional, default is 'column')
    group_by='ticker',

    # adjust all OHLC automatically
    # (optional, default is False)
    auto_adjust=True,

    # download pre/post regular market hours data
    # (optional, default is False)
    prepost=True,

    # use threads for mass downloading? (True/False/Integer)
    # (optional, default is True)
    threads=True,

    # proxy URL scheme use use when downloading?
    # (optional, default is None)
    proxy=None
)'''


def get_data(ticker):
    global days
    build_days(ticker)
    # if days == [], system up to date
    # load_days(ticker)


def build_days(ticker):
    global days
    data = []
    while True:
        try:
            data = yf.download(tickers=ticker,
                               period="max",
                               interval="1d",
                               group_by='ticker',
                               auto_adjust=True,
                               prepost=True,
                               threads=True,
                               proxy=None)
            data = data.dropna()
            if not os.path.isfile(database_loca + ticker + '.csv'):
                if len(data) != 0:
                    data.to_csv(days_loca + ticker + '.csv')
                    f = open(days_loca + ticker + '.csv', 'r')
                    reader = csv.reader(f)
                    list_day = []
                    days = []
                    for row in reader:
                        list_day.append(row)
                    for i in range(len(list_day)):
                        days.append(list_day[i][0])
                    # print(days)
                    del days[0]  # remove title for list
                    print('days: ', days)
                    break
                else:
                    showerror(title='Yahoo Error',
                              message='The information you requested for\n'
                                      'does not exist on yahoo finance,\n'
                                      'please try a different stock ticker.')
                    break
            else:
                if len(data) != 0:
                    data.to_csv(days_loca + ticker + '.csv')
                    file = open(days_loca + ticker + '.csv', 'r')
                    reader = csv.reader(file)
                    list_day = []
                    days = []
                    for row in reader:
                        list_day.append(row)
                    for i in range(len(list_day)):
                        days.append(list_day[i][0])
                    # print(days)
                    del days[0]  # remove title for list
                    file = open(database_loca + ticker + '.csv', 'r')
                    database_file = file.read()
                    file.close()
                    database_file = database_file.split('\n')
                    last_day = database_file[len(database_file) - 2]
                    last_day = last_day.split(',')
                    last_day = last_day[0]
                    last_day = last_day.replace('/', '-')
                    last_day = last_day.split('-')
                    if len(last_day[0]) == 1:
                        last_day[0] = '0' + last_day[0]
                    if len(last_day[1]) == 1:
                        last_day[1] = '0' + last_day[1]
                    last_day = last_day[2] + '-' + last_day[0] + '-' + last_day[1]
                    print('last_day: ', last_day)
                    date = datetime.now()
                    date_now = date.strftime("%G") + '-' + date.strftime("%m") + '-' + date.strftime("%d")
                    print('today: ', date_now)
                    print('days total: ', days)
                    days = days[days.index(last_day) + 1:]
                    print('days: ', days)
                    break
                else:
                    showerror(title='Yahoo Error',
                              message='The information you requested for\n'
                                      'does not exist on yahoo finance,\n'
                                      'please try a different stock ticker.')
                    break
        except:
            pass

    # find the last day in offline database scan only between then and now


def load_days(ticker):
    global days
    data = []
    print('here')
    [print(day) for day in days]
    for day in days:
        while True:
            try:
                data = yf.download(tickers=ticker,
                                   start=day,
                                   end=day,
                                   interval="5m",
                                   group_by='ticker',
                                   auto_adjust=True,
                                   prepost=True)
                data = data.dropna()
                print('data: ', data)
                data.to_csv(temp_loca + 'temp.csv')
                f = open(temp_loca + 'temp.csv', 'r')
                reader = csv.reader(f)
                list_day = []
                days = []
                for row in reader:
                    list_day.append(row)
                for i in range(len(list_day)):
                    days.append(list_day[i][0])
                # print(days)
                del days[0]  # remove title for list
                print('###')
                print(days)
            except:
                pass


get_data('SPY')
