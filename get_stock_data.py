import pandas_datareader as pdr


# -----------------get data fro yahoo for a given period------------------------------------
def get_stock_data(ticker_symbol, start_date):
    try:
        df = pdr.get_data_yahoo(ticker_symbol, start_date)
        return df
    except ValueError:
        print("invalid input")
