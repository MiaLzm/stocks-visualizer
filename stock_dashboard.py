# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
from stocks import Stocks
from stock_analyzer import Analyzer
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns
import datetime
from datetime import date
import os.path
from dateutil.relativedelta import relativedelta # to add days or years

# initialize stocks object to load data from the beginning of the chosen year to current date
stocks = Stocks(1980)

# retrieve and save stocks data (if trading data has not been saved)
if not os.path.exists('datasets/stocks'):
    stocks.save_stock_files()


companies = stocks.get_all_tickers_overview() # retrieves companies and descriptions, autofils NaNs
companies = companies.set_index('Symbol')


# dictionary to hold filter parameters
params = dict()


# ----------------- Build UI filter menu ------------------------------#
# create sets to store unique instances to populate select boxes
sectors = set(companies.loc[:,"Sector"])
stock_name = sorted(set(companies.loc[:, "Name"]))
stock_name.insert(0, "")

st.write("""
         # Stock analyzer
         Select a stock of interest to see its historical data. \
             Use the Sector to identify stocks of interest.
         """)

stock = st.sidebar.selectbox("Search for a stock (Option 1) type ahead single select", stock_name, index=0)
stock_two = st.sidebar.multiselect("Search for a stock (Option 2) type ahead multi-select", options = stock_name)

st.sidebar.write("--------------")
st.sidebar.write("Filters")
sector = st.sidebar.selectbox("Choose a sector", sectors)
params["Sector"] = sector
# filter stocks dropdown based on sector
ticker_syms = companies.loc[companies['Sector'] == sector]
ticker = st.sidebar.selectbox("Choose a stock", ticker_syms.index)
params["Stock"] = ticker
params["Company"] = companies.loc[companies.index == ticker ]
params["Company name"] = companies.loc[companies.index == ticker].Name


# company details
st.write(f"""## *{params["Stock"]}*""")
st.write(params["Company"])


# ------------------ Load dataset from filter parameters -----------#
todayDt = date.today()
#df = stocks.get_ticker_trading_history(params['Stock']) 
df = stocks.get_trading_history(params['Stock'], 
                                stocks.START_DATE, 
                                todayDt)


# format date to timestamp
df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')


# ensure to report trading Volume in millions
if not 'Volume (millions)' in df:
    stocks.clean_data(df)


#TODO: show how old the data is - and provide a refresh      
# pull in daily data
st.sidebar.button("Refresh")

# ------------------ Create floorplans -----------------------------#
col1, col2 = st.columns(2)
# ------------------ Plot data using filter parameters -------------#
visualizations = ["Stock price", "Stock Volume", "Moving averages"]


# filter dates
st.selectbox("Historical perspective", ["10 years", "5 years", "1 year", "6 months", "3 months", "1 month"])

# --- time series plot function - Matplotlib --- #
def plot_time_series(title, y_label, Y, col, df = df):
    # set plot font
    font = {'family': 'normal',
            'weight': 'normal',
            'size': 8
            }
    matplotlib.rc('font', **font)
    
    
    # timeline for each stock
    #TODO: convert dates from timestamp to %Y-%m-%d
    start_date = df.index[0]
    end_date = df.index[len(df)-1]
    pd.plotting.plot_params = {'x_compat': True,}
    fig, ax = plt.subplots()
    fig.set_figheight(2)
    plt.plot(Y)
    ax.set(
           xlabel = "date",
           ylabel = y_label,
           title = f"""{ticker} {title} {start_date} - {end_date}""",
           xlim = (start_date, end_date)
          )
    # TODO: make x,y axis labels smaller
    plt.xticks(rotation=90)
    plt.grid()
    fig.canvas.toolbar_visible = True
    fig.canvas.header_visible = True
    col.area_chart(Y)
    
    # return filter date range
    return start_date, end_date

# --- time series plot function - Seaborn --- #
def plot_timeseries_sns(title, y_label, y, df = df):
    # create timeline for each stock
    # TODO: this is returning int -- convert to date
    start_date = df.Date[0]
    end_date = df.Date[len(df)-1]
    
    # plot selected timeframe
    fig = plt.figure()
    fig.set_figheight(2)
    sns.lineplot(df.index, y)
    plt.xticks(rotation = 90)
    st.pyplot(fig)
    return start_date, end_date


# --- stock price --- #
col1.write(f"{params['Company']['Name']}")
price_start, price_end = plot_time_series('stock price', 'USD ($)', df["Adj Close"], col1)

# --- stock volume --- #
col2.write(f"{params['Company']['Name']}")
volume_start, volume_end = plot_time_series('trading volume', 'shares (millions)', df.iloc[:,4], col2)


# retrieve the last 5 trading days
st.write(f"""## *{params['Stock']}* 5-day Performance """)
st.write(df.tail(5))

# ---------------------- Stock performance KPIs ---------------------#
date_price = st.date_input("Select a date")
analyze = Analyzer(df, price_start, price_end)
day_price = analyze.get_day_price(date_price)
st.print(f"Stock price on {date_price} was {day_price}")




