#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 15:48:49 2021

@author: daire
"""
import pandas as pd
import os
from pandas_datareader import data

class Stocks(object):
    """
        Class that retrieves and manages stock trading data
    """
    def __init__(self):
        # path to data files
        self.STOCKS_BASE_PATH = os.path.join("datasets", "stocks")
        self.STOCKS_DIR = os.makedirs(self.STOCKS_BASE_PATH, exist_ok=True)
        
        
        # financial data source
        self.STOCK_SOURCE = 'yahoo'
        self.START_DATE = '2021-01-01'
        
        
        # list of companies
        self.TICKER_OVERVIEW = pd.DataFrame(pd.read_csv("nasdaq_screener.csv"))
        self.stocks_list = [] # populates UI with 
        
    
    def save_trading_data(self, ticker_sym):
        """
        
        Retrieve trading data for a single trading entity
        Parameters
        ----------
        ticker_sym : String
            Trading entity.

        Returns
        -------
        None.

        """
        try:
            stock = data.DataReader(ticker_sym, self.STOCK_SOURCE, self.START_DATE)
            stock.to_csv(self.STOCKS_BASE_PATH + f"/{ticker_sym}.csv")
            print("Retrieved stock history for ", ticker_sym)
            self.stocks_list.append(ticker_sym) # add ticker to valid list (for UI)
        except Exception as e :
           print(f"Could not retrieve stock for {ticker_sym}. {e}")
                    
            
    # function to retrieve stock from listed companies
    def save_stock_files(self):
        """
        Retrieve and save a file trading entities from a list of trading companies.
    
        Returns
        -------
        None.
    
        """
        # loop through a file containing a list of trading companies
        for ticker in self.TICKER_OVERVIEW.iloc[:,0]:
            self.save_trading_data(str(ticker)) # need to find earliest date for the stock
    
    
    def get_all_trading_history(self, ticker):
        """
        Function that retrieves trading data from saved files for a trading entity

        Parameters
        ----------
        ticker : String
            Trading entity.

        Returns
        -------
        trading_history : Data Frame
            Trading data for teh selected period.

        """
        # open the source file and return it as a DF
        try:
            trading_history = pd.read_csv(f"datasets/stocks/{ticker}.csv")
        except FileNotFoundError:
                trading_history = self.data.DataReader(ticker, self.STOCK_SOURCE, self.START_DATE)
        print("Retrieved ", len(trading_history), " rows for ", ticker)
        return trading_history
     

    def get_trading_history(self, ticker, startDt, endDt):
        """
        Function that retrieves trading data from saved files between two dates for a trading entity

        Parameters
        ----------
        ticker : String
            Trading entity.
        fromDt : Date
            Start date for historical trading data.
        toDt : Date
            End date for historical trading data.

        Returns
        -------
        trading_history : Data Frame
            Trading data for teh selected period.

        """
        # open the source file and return it as a DF
        try:
            trading_history = pd.read_csv(f"datasets/stocks/{ticker}.csv")
            print("Retrieved ", len(trading_history), " rows for ", ticker, "between ", startDt, " and ", endDt)
        except FileNotFoundError:
                trading_history = self.data.DataReader(ticker, self.STOCK_SOURCE, startDt)
        trading_history = trading_history[(trading_history['Date'] >= startDt) & (trading_history['Date'] <= endDt)]
        return trading_history                 
        
def main():
    stocks = Stocks()
    # stocks.save_stock_files()
    stocks.save_trading_data("GOOG")
    goog = stocks.get_all_trading_history("GOOG")
    googDt = stocks.get_trading_history('GOOG', '2021-01-01', '2021-06-01')
    
if __name__ == '__main__':
    # we are calling the amin function
    main()