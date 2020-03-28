from vader_sentiment import vaderParagraph, vaderAtOnce
import re
import os
import csv
import pandas as pd
from words import getKeyWords
import csv
from slugify import slugify
from datetime import datetime, timedelta, date
import os.path
from os import path
from statistics import mean

stock_dict = {"Bajaj": {"company": "Bajaj", "symbol": "BAJAJ-AUTO", "sector": "Automobile"}, "Eicher": {"company": "Eicher", "symbol": "EICHERMOT", "sector": "Automobile"}, "Hero": {"company": "Hero", "symbol": "HEROMOTOCO", "sector": "Automobile"}, "Mahindra": {"company": "Mahindra", "symbol": "M&M", "sector": "Automobile"}, "Maruti": {"company": "Maruti", "symbol": "MARUTI", "sector": "Automobile"}, "Tata Motors": {"company": "Tata Motors", "symbol": "TATAMOTORS", "sector": "Automobile"}, "Axis Bank": {"company": "Axis Bank", "symbol": "AXISBANK", "sector": "Banking"}, "HDFC": {"company": "HDFC", "symbol": "HDFCBANK", "sector": "Banking"}, "ICICI": {"company": "ICICI", "symbol": "ICICIBANK", "sector": "Banking"}, "IndusInd": {"company": "IndusInd", "symbol": "INDUSINDBK", "sector": "Banking"}, "Kotak Mahindra": {"company": "Kotak Mahindra", "symbol": "KOTAKBANK", "sector": "Banking"}, "State Bank of India": {"company": "State Bank of India", "symbol": "SBIN", "sector": "Banking"}, "Grasim": {"company": "Grasim", "symbol": "GRASIM", "sector": "Cement"}, "UltraTech": {"company": "UltraTech", "symbol": "ULTRACEMCO", "sector": "Cement"}, "Shree": {"company": "Shree", "symbol": "SHREECEM", "sector": "Cement"}, "United Phosphorus": {"company": "United Phosphorus", "symbol": "UPL", "sector": "Chemicals"}, "Larsen & Toubro": {"company": "Larsen & Toubro", "symbol": "LT", "sector": "Construction"}, "Asian Paints": {"company": "Asian Paints", "symbol": "ASIANPAINT", "sector": "Consumer Goods"}, "Hindustan Unilever": {"company": "Hindustan Unilever", "symbol": "HINDUNILVR", "sector": "Consumer Goods"}, "Britannia": {"company": "Britannia", "symbol": "BRITANNIA", "sector": "Consumer Goods"}, "ITC": {"company": "ITC", "symbol": "ITC", "sector": "Consumer Goods"}, "Titan": {"company": "Titan", "symbol": "TITAN", "sector": "Consumer Goods"}, "BPCL": {"company": "BPCL", "symbol": "BPCL", "sector": "Energy"}, "GAIL": {"company": "GAIL", "symbol": "GAIL", "sector": "Energy"}, "IOC": {"company": "IOC", "symbol": "IOC", "sector": "Energy"}, "ONGC": {"company": "ONGC", "symbol": "ONGC", "sector": "Energy"},
              "Reliance": {"company": "Reliance", "symbol": "RELIANCE", "sector": "Energy"}, "NTPC": {"company": "NTPC", "symbol": "NTPC", "sector": "Power"}, "PowerGrid Corporation of India": {"company": "PowerGrid Corporation of India", "symbol": "POWERGRID", "sector": "Power"}, "Coal India": {"company": "Coal India", "symbol": "COALINDIA", "sector": "Mining"}, "Bajaj Finance": {"company": "Bajaj Finance", "symbol": "BAJFINANCE", "sector": "Financial Services"}, "Bajaj Finserv": {"company": "Bajaj Finserv", "symbol": "BAJAJFINSV", "sector": "Financial Services"}, "HDFC": {"company": "HDFC", "symbol": "HDFC", "sector": "Financial Services"}, "Nestle India Ltd": {"company": "Nestle India Ltd", "symbol": "NESTLEIND", "sector": "Food Processing"}, "HCL": {"company": "HCL", "symbol": "HCLTECH", "sector": "Information Technology"}, "Infosys": {"company": "Infosys", "symbol": "INFY", "sector": "Information Technology"}, "Tata Consultancy Services": {"company": "Tata Consultancy Services", "symbol": "TCS", "sector": "Information Technology"}, "Tech Mahindra": {"company": "Tech Mahindra", "symbol": "TECHM", "sector": "Information Technology"}, "Wipro": {"company": "Wipro", "symbol": "WIPRO", "sector": "Information Technology"}, "Adani": {"company": "Adani", "symbol": "ADANIPORTS", "sector": "Infrastructure"}, "Zee": {"company": "Zee", "symbol": "ZEEL", "sector": "Media"}, "Hindalco": {"company": "Hindalco", "symbol": "HINDALCO", "sector": "Metals"}, "JSW": {"company": "JSW", "symbol": "JSWSTEEL", "sector": "Metals"}, "Tata Steel": {"company": "Tata Steel", "symbol": "TATASTEEL", "sector": "Metals"}, "Vedanta": {"company": "Vedanta", "symbol": "VEDL", "sector": "Metals"}, "Cipla": {"company": "Cipla", "symbol": "CIPLA", "sector": "Pharmaceuticals"}, "Dr Reddy": {"company": "Dr Reddy", "symbol": "DRREDDY", "sector": "Pharmaceuticals"}, "Sun Pharmaceutical": {"company": "Sun Pharmaceutical", "symbol": "SUNPHARMA", "sector": "Pharmaceuticals"}, "Airtel": {"company": "Airtel", "symbol": "BHARTIARTL", "sector": "Telecommunication"}, "Infratel": {"company": "Infratel", "symbol": "INFRATEL", "sector": "Telecommunication"}}

global final_dict
global relevant_docs
global retrieved_docs

final_dict = dict()
relevant_docs = 0
retrieved_docs = 0


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
            return(0, 0, 0, "invalid")

    effect = ""
    if(perc_change > 0):
        effect = "Positive"
    elif(perc_change < 0):
        effect = "Negative"
    else:
        effect = "Neutral"

    # print(perc_change, open_val, close_val, effect)
    return(perc_change, open_val, close_val, effect)


def addDay(day):
    dt_object = datetime.strptime(day, "%Y-%m-%d")
    date1 = dt_object + timedelta(days=1)
    timestamp = datetime.timestamp(date1)
    date_time = datetime.fromtimestamp(timestamp)
    d = date_time.strftime("%Y-%m-%d")
    return(d)


def getCsvRows(inputFile, newsPaper):
    global final_dict

    inputFileOpen = open('../data/news/'+newsPaper+"/" +
                         inputFile, 'r', encoding="utf8")
    inputFile = csv.reader(inputFileOpen)

    prints = 0

    global relevant_docs
    global retrieved_docs

    for idx, row in enumerate(inputFile):
        retrieved_docs = retrieved_docs+1

        # if(idx < 100):
        #     continue
        if(idx > 100):
            break
        if(row[0] == ""):
            continue
        if(idx % 100 == 0):
            print("{} iterations done".format(idx))
            # print(row[2])

        headline, link, vader_score, stocks_arr, sectors_arr, dates = getPolarityScore(
            row, newsPaper)

        dates = str(dates)

        entered_stock = False

        if stocks_arr != []:
            entered_stock = True
            relevant_docs = relevant_docs+1

            stocks_arr = stocks_arr.split("|")

            if not dates in final_dict:
                final_dict[dates] = {"sector": {}}
            for stock in stocks_arr:
                if not stock in final_dict[dates]:
                    final_dict[dates][stock] = {
                        'vader': [], 'link': [], 'headline': []}
                final_dict[dates][stock]['vader'].append(vader_score)
                final_dict[dates][stock]['link'].append(link)
                final_dict[dates][stock]['headline'].append(headline)

            if sectors_arr != [] and sectors_arr != " ":
                sectors_arr = sectors_arr.strip().split("|")
                for sector in sectors_arr:
                    if not sector in final_dict[dates]["sector"]:
                        final_dict[dates]["sector"][sector] = []
                    final_dict[dates]["sector"][sector].append(vader_score)

        # if not entered_stock and sectors_arr != []:
        #     f = 0


def getPolarityScore(row, newsPaper):
    raw_file_data = ""
    vader_score = 0

    raw_heading = str(slugify(row[0]))
    raw_news_file = raw_heading[0:120]+"-"+str(slugify(row[2]))
    raw_file_name = '../data/news/'+newsPaper+'/raw/'+raw_news_file+'.txt'
    url = row[1]

    if(path.exists(raw_file_name)):
        raw_file = open(raw_file_name, "r", encoding="utf8").read()
        raw_file_split = raw_file.split("-------")
        raw_file_heading = raw_file_split[0]
        raw_file_data = raw_file_split[1]
        raw_file_heading = raw_file_heading.replace("--", ",")
        vader_score = vaderParagraph(raw_file_heading, raw_file_data)
        vader_polarity = "Neutral news"
        news_data = raw_file_data.replace("\n", "")
        keyWords, keySectors = getKeyWords(news_data)

        return(raw_file_heading, url, vader_score, keyWords, keySectors, row[2])


def makeKeyWordList():
    global final_dict

    global relevant_docs
    global retrieved_docs

    # getCsvRows('moneyctl-merged-buisness.csv', "moneycontrol")
    # getCsvRows('economic-merged-formatted.csv', "economic")
    # getCsvRows('economic-merged.csv', "economic")
    getCsvRows('deccan-business.csv', "deccan")
    # getCsvRows('firstpost-merged.csv', "firstpost")

    tp, tn, fp, fn = 0, 0, 0, 0

    for dates in final_dict:
        for index in final_dict[dates]:

            if(index == "sector"):
                # print(final_dict[dates]["sector"])
                continue
            stock_avg_score = round(
                mean(final_dict[dates][index]['vader']), 2)

            symbol, industry, sector = (getSymbol(index.strip()))
            perc_change, open_val, close_val, effect = getStockPrice(
                getStockFile(symbol), dates)

            if(effect == "invalid"):
                continue

            if (perc_change > 0 and stock_avg_score > 0):
                tp = tp+1
            elif(perc_change < 0 and stock_avg_score < 0):
                tn = tn+1
            elif(perc_change < 0 and stock_avg_score > 0):
                fp = fp+1

            elif(perc_change > 0 and stock_avg_score < 0):
                fn = fn+1

    # print("\n\nConfusion matrix: \nTP: {}\tFP: {}\nFN: {}\tTN: {}\n".format(
    #     tp, fp, fn, tn))

    precision = round(
        (retrieved_docs / (relevant_docs + retrieved_docs))*100, 2)
    recall = round((relevant_docs / (relevant_docs + retrieved_docs))*100, 2)

    acc = round(((tn+tp)/(tp+tn+fp+fn))*100, 4)
    specificity = round((tn/(tn + fp))*100, 2)
    sensitivity = round((tp/(tp + fn))*100, 2)

    # print("Accuracy = {}%".format(acc))
    # print("Specificity = {}".format(specificity))
    # print("Sensitivity = {}".format(sensitivity))
    # print("Retrieved = {}, Relevant = {}".format(retrieved_docs, relevant_docs))
    # print("Precision = {}".format(precision))
    # print("Recall = {}".format(recall))

    # print(index, stock_avg_score, perc_change)


def main():
    index, company, sector = getSymbol("Bajaj")
    getStockPrice(getStockFile(index), "2019-07-28")


makeKeyWordList()
