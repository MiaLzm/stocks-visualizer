# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
from stocks import Stocks
from stock_analyzer import Analyzer
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns
import datetime
import os.path
from dateutil.relativedelta import relativedelta # to add days or years

# initialize stocks object to load data from the beginning of the chosen year to current date
stocks = Stocks(2018)

# retrieve and save stocks data (if trading data has not been saved)
if not os.path.exists('datasets/stocks'):
    stocks.save_stock_files()


companies = stocks.get_all_tickers_overview() # retrieves companies and descriptions, autofils NaNs
companies.reset_index(drop=True)
companies.set_index('Symbol')


# dictionary to hold filter parameters
params = dict()


# ----------------- Build UI elements ------------------------------#
# create sets to store unique instances to populate select boxes
sectors = set(companies.loc[:,"Sector"])

st.write("""
         # Stock analyzer
         Select a stock of interest to see its historical data. \
             Use the Sector to identify stocks of interest.
         """)

sector = st.sidebar.selectbox("Choose a sector", sectors)
params["Sector"] = sector


# filter stocks dropdown based on sector
ticker_syms = companies.loc[companies['Sector'] == sector]
ticker = st.sidebar.selectbox("Choose a stock", ticker_syms)
params["stock"] = ticker
params["company"] = companies.loc[companies["Symbol"] == ticker ]


# company details
st.write(f"""## *{params["stock"]}*""")
st.write(params["company"])


# ------------------ Load dataset from filter parameters -----------#
df = stocks.get_ticker_trading_history(params['stock']) 
#df = stocks.get_trading_history(params['stock'], stocks.START_DATE, datetime.datetime.now().strftime("Y-%m-%d"))


# format date to timestamp
df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')


# report trading Volume in millions
df['Volume'] = df.Volume/1000000
df = df.rename(columns={'Volume': 'Volume (millions)'})

# set trading period
start_date = df.index[0]
end_date = df.index[len(df)-1]
periodRange = st.sidebar.date_input("Period Range", min_value=start_date)

## Range selector
format = 'MMM DD, YYYY'  # format output
start_date = datetime.date(year=2021,month=1,day=1)-relativedelta(years=20)  #  I need some range in the past
end_date = datetime.datetime.now().date()-relativedelta(years=2)
max_days = end_date-start_date
        
# pull in daily data
st.sidebar.button("Refresh")


# ------------------ Plot data using filter parameters -------------#
# --- time series plot function - Matplotlib ---
def plot_time_series(title, y_label, Y, df = df):
    # timeline for each stock
    start_date = df.index[0]
    end_date = df.index[len(df)-1]
    pd.plotting.plot_params = {'x_compat': True,}
    fig, ax = plt.subplots()
    fig.set_figheight(2)
    plt.plot(df.index, Y)
    ax.set(
           xlabel = "date",
           ylabel = y_label,
           title = f"""{ticker} {title} {start_date} - {end_date}""",
           xlim = (start_date, end_date)
          )
    # TODO: make x,y axis labels smaller
    plt.xticks(rotation=90)
    st.pyplot(fig)

def plot_timeseries_sns(title, y_label, y, df = df):
    # create timeline for each stock
    start_date = df.index[0]
    end_date = df.index[len(df)-1]
    
    # plot selected timeframe
    fig = plt.figure()
    fig.set_figheight(2)
    sns.lineplot(df.index, y)
    plt.xticks(rotation = 90)
    st.pyplot(fig)
    
# --- stock price --- #
# stock_price_series = plot_time_series('stock price', 'USD ($)', df.Close)
stock_price_series = plot_timeseries_sns('stock price', 'USD ($)', df.Close)


# --- stock volume --- #
# volume_series = plot_time_series('trading volume', 'shares (millions)', df['Volume (millions)'])
volume_series = plot_timeseries_sns('trading volume', 'shares (millions)', df['Volume (millions)'])


# filter dates
slider = st.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
## Sanity check
st.table(pd.DataFrame([[start_date, slider, end_date]],
              columns=['start',
                       'selected',
                       'end'],
              index=['date']))


# retrieve the last 5 trading days
st.write(f"""## *{params['stock']}* 5-day Performance """)
st.write(df.tail(5))

# ---------------------- Stock performance KPIs ---------------------#
analyze = Analyzer(df, start_date, end_date)
open_day = analyze.get_day_price('2021-10-28')




