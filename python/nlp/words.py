from vader_sentiment import vaderAtOnce
import urllib
import requests
import pandas as pd
import time

data_list = ["Bajaj Auto", "Eicher Motors", "Hero MotoCorp", "Mahindra", "Maruti Suzuki", "Tata Motors", "Axis Bank", "HDFC Bank", "ICICI Bank", "IndusInd Bank", "Kotak Mahindra Bank", "State Bank of India", "Grasim Industries", "UltraTech Cement", "Shree Cement", "United Phosphorus Limited", "Larsen & Toubro", "Asian Paints Ltd", "Hindustan Unilever", "Britannia Industries", "ITC Limited", "Titan Company", "BPCL", "GAIL", "IOC",
             "ONGC", "Reliance Industries", "NTPC Limited", "PowerGrid Corporation of India", "Coal India", "Bajaj Finance", "Bajaj Finserv", "HDFC", "Nestle India Ltd", "HCL Technologies", "Infosys", "Tata Consultancy Services", "Tech Mahindra", "Wipro", "Adani Ports", "Zee Entertainment Enterprises", "Hindalco", "JSW Steel", "Tata Steel", "Vedanta", "Cipla", "Dr Reddy Lab", "Sun Pharmaceutical", "Airtel", "Infratel"]

data_list_custom = ["Bajaj", "Eicher", "Hero", "Mahindra", "Maruti Suzuki", "Tata Motors", "Axis Bank", "HDFC", "ICICI", "IndusInd", "Kotak Mahindra", "State Bank of India", "Grasim", "UltraTech", "Shree", "United Phosphorus", "Larsen & Toubro", "Asian Paints", "Hindustan Unilever", "Britannia", "ITC", "Titan", "BPCL",
                    "GAIL", "IOC", "ONGC", "Reliance", "NTPC", "PowerGrid Corporation of India", "Coal", "Bajaj Finance", "Bajaj Finserv", "HDFC", "Nestle India Ltd", "HCL", "Infosys", "Tata Consultancy Services", "Tech Mahindra", "Wipro", "Adani", "Zee", "Hindalco", "JSW", "Tata Steel", "Vedanta", "Cipla", "Dr Reddy", "Sun Pharmaceutical", "Airtel", "Infratel"]

sector_list = ["Automobile", "Automobile", "Automobile", "Automobile", "Automobile", "Automobile", "Banking", "Banking", "Banking", "Banking", "Banking", "Banking", "Cement", "Cement", "Cement", "Chemicals", "Construction", "Consumer Goods", "Consumer Goods", "Consumer Goods", "Consumer Goods", "Consumer Goods", "Energy", "Energy", "Energy", "Energy", "Energy", "Power", "Power", "Mining",
               "Financial Services", "Financial Services", "Financial Services", "Food Processing", "Information Technology", "Information Technology", "Information Technology", "Information Technology", "Information Technology", "Infrastructure", "Media & Entertainment", "Metals", "Metals", "Metals", "Metals", "Pharmaceuticals", "Pharmaceuticals", "Pharmaceuticals", "Telecommunication", "Telecommunication"]

stock_list = ["BAJAJ-AUTO", "EICHERMOT", "HEROMOTOCO", "M&M", "MARUTI", "TATAMOTORS", "AXISBANK", "HDFCBANK", "ICICIBANK", "INDUSINDBK", "KOTAKBANK", "SBIN", "GRASIM", "ULTRACEMCO", "SHREECEM", "UPL", "LT", "ASIANPAINT", "HINDUNILVR", "BRITANNIA", "ITC", "TITAN", "BPCL", "GAIL",
              "IOC", "ONGC", "RELIANCE", "NTPC", "POWERGRID", "COALINDIA", "BAJFINANCE", "BAJAJFINSV", "HDFC", "NESTLEIND", "HCLTECH", "INFY", "TCS", "TECHM", "WIPRO", "ADANIPORTS", "ZEEL", "HINDALCO", "JSWSTEEL", "TATASTEEL", "VEDL", "CIPLA", "DRREDDY", "SUNPHARMA", "BHARTIARTL", "INFRATEL"]

inputData = "Hello world in mahindra"
vaderAtOnce("Hello world is positive")

start = time.time()
for word, idx in enumerate(data_list_custom):
    if (word.lower() in inputData.lower()):
        print(word)

end = time.time() - start
