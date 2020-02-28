# from yahoo_finance import Share
# import requests
# yahoo = Share('COALINDIA.NS')
# print(yahoo.get_open())


import yfinance as yf
msft = yf.Ticker("COALINDIA.NS")
# print(msft.info)
hist = msft.history(period="max")
print(hist)
