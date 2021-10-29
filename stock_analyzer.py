# -*- coding: utf-8 -*-
from stocks import Stocks
import numpy as np

class Analyzer():
    """
        Class that receives stock trading data and returns KPIs
    """
    
    def __init__(self, stock_df, period_start, period_end):
        """
        Parameters
        ----------
        stock : Dataframe
            Dataframe containing trading data for a stock
        period_start : Date
            Financial period start date
        period_end : Date
            Financial period end date

        Returns
        -------
        None.

        """
        
        self.STOCK_DF = stock_df
        self.start = period_start
        self.end = period_end
        
    def mean(self, startDt, endDt, series):
        return np.mean(series)
    
    def range(self, startDt, endDt, series):
        range(series[0], series(len(series)-1))
    
    def get_day_price(self, dt):
        price = self.STOCK_DF.loc[self.STOCK_DF.index == dt].Close[0]
        return price # add error handling
        
        