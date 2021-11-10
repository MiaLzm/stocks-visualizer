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
stock_list = sorted(set(companies.loc[:, "Name"]))
stock_list.insert(0, "")

st.write("""
         # Stock analyzer
         Select a stock of interest to see its historical data. \
             Use the Sector to identify stocks of interest.
         """)

stock_name = st.sidebar.selectbox("Search for a stock (Option 1) type ahead single select", stock_list, index=0)
stock_two = st.sidebar.multiselect("Search for a stock (Option 2) type ahead multi-select", options = stock_list)
'''params["Stock"] = companies.loc[companies.Name == stock_name]["Sector"]
params["Company"] = stock_name'''

st.sidebar.write("--------------")
st.sidebar.write("Filters")
sector = st.sidebar.selectbox("Choose a sector", sectors)
params["Sector"] = sector
# filter stocks dropdown based on sector
ticker_syms = companies.loc[companies['Sector'] == sector]
ticker = st.sidebar.selectbox("Choose a stock", ticker_syms.index)
params["Stock"] = ticker
params["Company"] = companies.loc[companies.index == ticker ]
params["Company name"] = companies.loc[companies.index == ticker]['Name'].item()


# company details
st.write(f"""## *{params["Stock"]}*""")
st.write(params["Company"])


# ------------------ Load dataset from filter parameters -----------#
todayDt = date.today()
df = stocks.get_trading_history(params['Stock'], 
                                stocks.START_DATE, 
                                todayDt)


# set date as the index and format date to timestamp

df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')


# ensure to report trading Volume in millions
'''if not 'Volume (millions)' in df:
    stocks.clean_data(df)'''


#TODO: show how old the data is - and provide a refresh      
# pull in daily data
st.sidebar.button("Refresh")

# ------------------ Create floorplans -----------------------------#
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

# ------------------- chart selection ------------------------------#
visualizations = ["Stock price", "Stock volume", "Moving averages"]
selected_viz = col1.multiselect("Visualization", visualizations)

# -------------------- Date selection ------------------------------#
# filter dates
timeline = col2.selectbox("Time period", ["10 years", "5 years", "1 year", "6 months", "3 months", "1 month"])


# ------------------ Plot data using filter parameters -------------#


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
    date_format = mdates.DateFormatter('%Y')
    pd.plotting.plot_params = {'x_compat': True,}
    fig, ax = plt.subplots()
    fig.set_figheight(5)
    plt.plot(df.index, Y)
    ax.set(
           xlabel = "date",
           ylabel = y_label,
           title = f"""{ticker} {title}""",
           xlim = (start_date, end_date)
          )
    ax.xaxis.set_major_formatter(date_format)
    # TODO: decide on matplotlib or streamlit plot
    plt.xticks(rotation=90)
    plt.grid()
    fig.canvas.toolbar_visible = True
    fig.canvas.header_visible = True
        
    # draw a trend line
    slope, intercept = np.polyfit(mdates.date2num(df.index), Y, 1)
    reg_line = slope*mdates.date2num(df.index) + intercept
    plt.plot(df.index, reg_line)
    col.write(fig)
    
    
    # return filter date range
    return start_date, end_date

# --- time series plot function - Seaborn --- #
def plot_time_series_sns(title, y_label, y, col, df = df):
    # create timeline for each stock
    # TODO: this is returning int -- convert to date
    start_date = df.index[0]
    end_date = df.index[len(df)-1]
    
    # set aesthetics for the chart
    sns.set_theme()
    sns.set_style("darkgrid")
    sns.color_palette("bright")
    fig, ax = plt.subplots()
    ax.set_xlabel("Date", fontsize = 16)
    ax.set_ylabel(y_label, fontsize = 16)
    ax.set_title(f"{ticker} {title}", fontsize = 16)
    sns.regplot(x = mdates.date2num(df.index), y = y, 
                    data = df, fit_reg = True, marker='^', color = 'purple')
    #sns.lmplot(x = mdates.date2num(df.index), y = y, data = df, fit_reg = True)
    plt.xticks(rotation = 90)
    
    # format date axis
    date_formatter = DateFormatter('%Y')
    ax.xaxis.set_major_formatter(date_formatter)
    
    
    # plot selected timeframe
    col.pyplot(fig)
    return start_date, end_date


# --- stock price --- #
# Streamlit area plot
if 'Stock price' in selected_viz:
    price_start, price_end = plot_time_series('stock price', 'USD ($)', df["Adj Close"], col1)

    # Seaborn line plot with regression line
    price_start, price_end = plot_time_series_sns('stock price', 'USD ($)', df["Adj Close"], col3)

# --- stock volume --- #
if "Stock volume" in selected_viz:
    # area plot example
    volume_start, volume_end = plot_time_series('trading volume', 'shares (millions)', df.loc[:,'Volume'], col2)
    
    # Seaborn line plot with regression line
    volume_start, volume_end = plot_time_series_sns('trading volume', 'shares (millions)', df.loc[:,'Volume'], col4)

# retrieve the last 5 trading days
st.write(f"""## *{params['Stock']}* 5-day Performance """)
st.write(df.tail(5))

# ---------------------- Stock performance KPIs ---------------------#
date_price = st.date_input("Select a date")
#analyze = Analyzer(df, price_start, price_end)
#day_price = analyze.get_day_price(date_price)
#st.print(f"Stock price on {date_price} was {day_price}")




