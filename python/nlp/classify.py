from vader_sentiment import vaderParagraph, vaderAtOnce
import re
import os
import csv
import pandas as pd
from words import getKeyWords
import csv

from datetime import datetime, timedelta, date

stock_dict = {"Bajaj": {"company": "Bajaj", "symbol": "BAJAJ-AUTO", "sector": "Automobile"}, "Eicher": {"company": "Eicher", "symbol": "EICHERMOT", "sector": "Automobile"}, "Hero": {"company": "Hero", "symbol": "HEROMOTOCO", "sector": "Automobile"}, "Mahindra": {"company": "Mahindra", "symbol": "M&M", "sector": "Automobile"}, "Maruti": {"company": "Maruti", "symbol": "MARUTI", "sector": "Automobile"}, "Tata Motors": {"company": "Tata Motors", "symbol": "TATAMOTORS", "sector": "Automobile"}, "Axis Bank": {"company": "Axis Bank", "symbol": "AXISBANK", "sector": "Banking"}, "HDFC": {"company": "HDFC", "symbol": "HDFCBANK", "sector": "Banking"}, "ICICI": {"company": "ICICI", "symbol": "ICICIBANK", "sector": "Banking"}, "IndusInd": {"company": "IndusInd", "symbol": "INDUSINDBK", "sector": "Banking"}, "Kotak Mahindra": {"company": "Kotak Mahindra", "symbol": "KOTAKBANK", "sector": "Banking"}, "State Bank of India": {"company": "State Bank of India", "symbol": "SBIN", "sector": "Banking"}, "Grasim": {"company": "Grasim", "symbol": "GRASIM", "sector": "Cement"}, "UltraTech": {"company": "UltraTech", "symbol": "ULTRACEMCO", "sector": "Cement"}, "Shree": {"company": "Shree", "symbol": "SHREECEM", "sector": "Cement"}, "United Phosphorus": {"company": "United Phosphorus", "symbol": "UPL", "sector": "Chemicals"}, "Larsen & Toubro": {"company": "Larsen & Toubro", "symbol": "LT", "sector": "Construction"}, "Asian Paints": {"company": "Asian Paints", "symbol": "ASIANPAINT", "sector": "Consumer Goods"}, "Hindustan Unilever": {"company": "Hindustan Unilever", "symbol": "HINDUNILVR", "sector": "Consumer Goods"}, "Britannia": {"company": "Britannia", "symbol": "BRITANNIA", "sector": "Consumer Goods"}, "ITC": {"company": "ITC", "symbol": "ITC", "sector": "Consumer Goods"}, "Titan": {"company": "Titan", "symbol": "TITAN", "sector": "Consumer Goods"}, "BPCL": {"company": "BPCL", "symbol": "BPCL", "sector": "Energy"}, "GAIL": {"company": "GAIL", "symbol": "GAIL", "sector": "Energy"}, "IOC": {"company": "IOC", "symbol": "IOC", "sector": "Energy"}, "ONGC": {"company": "ONGC", "symbol": "ONGC", "sector": "Energy"},
              "Reliance": {"company": "Reliance", "symbol": "RELIANCE", "sector": "Energy"}, "NTPC": {"company": "NTPC", "symbol": "NTPC", "sector": "Power"}, "PowerGrid Corporation of India": {"company": "PowerGrid Corporation of India", "symbol": "POWERGRID", "sector": "Power"}, "Coal India": {"company": "Coal India", "symbol": "COALINDIA", "sector": "Mining"}, "Bajaj Finance": {"company": "Bajaj Finance", "symbol": "BAJFINANCE", "sector": "Financial Services"}, "Bajaj Finserv": {"company": "Bajaj Finserv", "symbol": "BAJAJFINSV", "sector": "Financial Services"}, "HDFC": {"company": "HDFC", "symbol": "HDFC", "sector": "Financial Services"}, "Nestle India Ltd": {"company": "Nestle India Ltd", "symbol": "NESTLEIND", "sector": "Food Processing"}, "HCL": {"company": "HCL", "symbol": "HCLTECH", "sector": "Information Technology"}, "Infosys": {"company": "Infosys", "symbol": "INFY", "sector": "Information Technology"}, "Tata Consultancy Services": {"company": "Tata Consultancy Services", "symbol": "TCS", "sector": "Information Technology"}, "Tech Mahindra": {"company": "Tech Mahindra", "symbol": "TECHM", "sector": "Information Technology"}, "Wipro": {"company": "Wipro", "symbol": "WIPRO", "sector": "Information Technology"}, "Adani": {"company": "Adani", "symbol": "ADANIPORTS", "sector": "Infrastructure"}, "Zee": {"company": "Zee", "symbol": "ZEEL", "sector": "Media"}, "Hindalco": {"company": "Hindalco", "symbol": "HINDALCO", "sector": "Metals"}, "JSW": {"company": "JSW", "symbol": "JSWSTEEL", "sector": "Metals"}, "Tata Steel": {"company": "Tata Steel", "symbol": "TATASTEEL", "sector": "Metals"}, "Vedanta": {"company": "Vedanta", "symbol": "VEDL", "sector": "Metals"}, "Cipla": {"company": "Cipla", "symbol": "CIPLA", "sector": "Pharmaceuticals"}, "Dr Reddy": {"company": "Dr Reddy", "symbol": "DRREDDY", "sector": "Pharmaceuticals"}, "Sun Pharmaceutical": {"company": "Sun Pharmaceutical", "symbol": "SUNPHARMA", "sector": "Pharmaceuticals"}, "Airtel": {"company": "Airtel", "symbol": "BHARTIARTL", "sector": "Telecommunication"}, "Infratel": {"company": "Infratel", "symbol": "INFRATEL", "sector": "Telecommunication"}}


def getStockFile(index):
    path = '../data/stocks/alphavantage/'+index
    df = pd.read_csv(path, parse_dates=['timestamp'], index_col=['timestamp'])
    return(df)


def getSymbol(data):
    index = stock_dict[data]
    return(index["symbol"], index["company"], index["sector"])


def getStockPrice(df, date):

    open_val = -1
    perc_change = 0
    close_val = 0
    while open_val < 0:
        try:
            open_val = (df.at[date, "open"][0])
            close_val = (df.at[date, "close"][0])
            perc_change = round(100 * (close_val - open_val) / open_val, 2)
        except:
            date = addDay(date)

    effect = ""
    if(perc_change > 0):
        effect = "Positive"
    elif(perc_change < 0):
        effect = "Negative"
    else:
        effect = "Neutral"
    print(perc_change, open_val, close_val, effect)


def main():
    print(stock_dict["Bajaj"]["symbol"])
    index, company, sector = getSymbol("Bajaj")
    getStockPrice(getStockFile(index), "2019-07-28")


def addDay(day):
    dt_object = datetime.strptime(day, "%Y-%m-%d")
    date1 = dt_object + timedelta(days=1)
    timestamp = datetime.timestamp(date1)
    date_time = datetime.fromtimestamp(timestamp)
    d = date_time.strftime("%Y-%m-%d")
    return(d)


def makeKeyWordList():
    main()
