# from yahoo_finance import Share
# import requests
# yahoo = Share('COALINDIA.NS')
# print(yahoo.get_open())


import yfinance as yf

stock_list = ["ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "BPCL.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "GAIL.NS", "GRASIM.NS", "HCLTECH.NS", "HDFC.NS", "HDFCBANK.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "IBULHSGFIN.NS",
              "ICICIBANK.NS", "INDUSINDBK.NS", "INFRATEL.NS", "INFY.NS", "IOC.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "MARUTI.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBIN.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "VEDL.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS"]


def getStockData(ticker):
    msft = yf.Ticker(ticker)
    # print(msft.info)
    hist = msft.history(period="1d", interval="10m")
    print(hist)


getStockData("COALINDIA.NS")
