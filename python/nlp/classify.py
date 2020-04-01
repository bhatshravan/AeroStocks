from vader_sentiment import vaderParagraph, vaderAtOnce
import re
import os
import csv
import pandas as pd
from words import getKeyWords
import csv
from slugify import slugify
from datetime import datetime, timedelta, date
import logging
import os.path
from os import path
from statistics import mean
import random
import combined as combined
from time import time
import multiprocessing

stock_dict = {
    "Bajaj Auto": {"company": "Bajaj", "symbol": "BAJAJ-AUTO", "sector": "Automobile"},
    "Eicher Motors": {"company": "Eicher", "symbol": "EICHERMOT", "sector": "Automobile"},
    "Hero MotoCorp": {"company": "Hero", "symbol": "HEROMOTOCO", "sector": "Automobile"},
    "Mahindra": {"company": "Mahindra", "symbol": "M&M", "sector": "Automobile"},
    "Maruti Suzuki": {"company": "Maruti", "symbol": "MARUTI", "sector": "Automobile"},
    "Tata Motors": {
        "company": "Tata Motors",
        "symbol": "TATAMOTORS",
        "sector": "Automobile",
    },
    "Axis Bank": {"company": "Axis Bank", "symbol": "AXISBANK", "sector": "Banking"},
    "HDFC Bank": {"company": "HDFC", "symbol": "HDFCBANK", "sector": "Banking"},
    "ICICI Bank": {"company": "ICICI", "symbol": "ICICIBANK", "sector": "Banking"},
    "IndusInd Bank": {"company": "IndusInd", "symbol": "INDUSINDBK", "sector": "Banking"},
    "Kotak Mahindra Bank": {
        "company": "Kotak Mahindra",
        "symbol": "KOTAKBANK",
        "sector": "Banking",
    },
    "State Bank of India": {
        "company": "State Bank of India",
        "symbol": "SBIN",
        "sector": "Banking",
    },
    "Grasim Industries": {"company": "Grasim", "symbol": "GRASIM", "sector": "Cement"},
    "UltraTech Cement": {"company": "UltraTech", "symbol": "ULTRACEMCO", "sector": "Cement"},
    "Shree Cement": {"company": "Shree", "symbol": "SHREECEM", "sector": "Cement"},
    "United Phosphorus Limited": {
        "company": "United Phosphorus",
        "symbol": "UPL",
        "sector": "Chemicals",
    },
    "Larsen & Toubro": {
        "company": "Larsen & Toubro",
        "symbol": "LT",
        "sector": "Construction",
    },
    "Asian Paints Ltd": {
        "company": "Asian Paints",
        "symbol": "ASIANPAINT",
        "sector": "Consumer Goods",
    },
    "Hindustan Unilever": {
        "company": "Hindustan Unilever",
        "symbol": "HINDUNILVR",
        "sector": "Consumer Goods",
    },
    "Britannia Industries": {
        "company": "Britannia",
        "symbol": "BRITANNIA",
        "sector": "Consumer Goods",
    },
    "ITC Limited": {"company": "ITC", "symbol": "ITC", "sector": "Consumer Goods"},
    "Titan Company": {"company": "Titan", "symbol": "TITAN", "sector": "Consumer Goods"},
    "BPCL": {"company": "BPCL", "symbol": "BPCL", "sector": "Energy"},
    "GAIL": {"company": "GAIL", "symbol": "GAIL", "sector": "Energy"},
    "IOC": {"company": "IOC", "symbol": "IOC", "sector": "Energy"},
    "ONGC": {"company": "ONGC", "symbol": "ONGC", "sector": "Energy"},
    "Reliance Industries": {"company": "Reliance", "symbol": "RELIANCE", "sector": "Energy"},
    "NTPC Limited": {"company": "NTPC", "symbol": "NTPC", "sector": "Power"},
    "PowerGrid Corporation of India": {
        "company": "PowerGrid Corporation of India",
        "symbol": "POWERGRID",
        "sector": "Power",
    },
    "Coal India": {"company": "Coal India", "symbol": "COALINDIA", "sector": "Mining"},
    "Bajaj Finance": {
        "company": "Bajaj Finance",
        "symbol": "BAJFINANCE",
        "sector": "Financial Services",
    },
    "Bajaj Finserv": {
        "company": "Bajaj Finserv",
        "symbol": "BAJAJFINSV",
        "sector": "Financial Services",
    },
    "HDFC": {"company": "HDFC", "symbol": "HDFC", "sector": "Financial Services"},
    "Nestle India Ltd": {
        "company": "Nestle India Ltd",
        "symbol": "NESTLEIND",
        "sector": "Food Processing",
    },
    "HCL Technologies": {"company": "HCL", "symbol": "HCLTECH", "sector": "Information Technology"},
    "Infosys": {
        "company": "Infosys",
        "symbol": "INFY",
        "sector": "Information Technology",
    },
    "Tata Consultancy Services": {
        "company": "Tata Consultancy Services",
        "symbol": "TCS",
        "sector": "Information Technology",
    },
    "Tech Mahindra": {
        "company": "Tech Mahindra",
        "symbol": "TECHM",
        "sector": "Information Technology",
    },
    "Wipro": {
        "company": "Wipro",
        "symbol": "WIPRO",
        "sector": "Information Technology",
    },
    "Adani Ports": {"company": "Adani", "symbol": "ADANIPORTS", "sector": "Infrastructure"},
    "Zee Entertainment Enterprises": {"company": "Zee", "symbol": "ZEEL", "sector": "Media"},
    "Hindalco": {"company": "Hindalco", "symbol": "HINDALCO", "sector": "Metals"},
    "JSW Steel": {"company": "JSW", "symbol": "JSWSTEEL", "sector": "Metals"},
    "Tata Steel": {"company": "Tata Steel", "symbol": "TATASTEEL", "sector": "Metals"},
    "Vedanta": {"company": "Vedanta", "symbol": "VEDL", "sector": "Metals"},
    "Cipla": {"company": "Cipla", "symbol": "CIPLA", "sector": "Pharmaceuticals"},
    "Dr Reddy Lab": {
        "company": "Dr Reddy",
        "symbol": "DRREDDY",
        "sector": "Pharmaceuticals",
    },
    "Sun Pharmaceutical": {
        "company": "Sun Pharmaceutical",
        "symbol": "SUNPHARMA",
        "sector": "Pharmaceuticals",
    },
    "Airtel": {
        "company": "Airtel",
        "symbol": "BHARTIARTL",
        "sector": "Telecommunication",
    },
    "Infratel": {
        "company": "Infratel",
        "symbol": "INFRATEL",
        "sector": "Telecommunication",
    },
}

sectorStockDict = {'Automobile': ['Bajaj Auto', 'Eicher Motors', 'Hero MotoCorp', 'Mahindra', 'Maruti Suzuki', 'Tata Motors'], 'Banking': ['Axis Bank', 'HDFC Bank', 'ICICI Bank', 'IndusInd Bank', 'Kotak Mahindra Bank', 'State Bank of India'], 'Cement': ['Grasim Industries', 'UltraTech Cement', 'Shree Cement'], 'Chemicals': ['United Phosphorus Limited'], 'Construction': ['Larsen & Toubro'], 'Consumer Goods': ['Asian Paints Ltd', 'Hindustan Unilever', 'Britannia Industries', 'ITC Limited', 'Titan Company'], 'Energy': ['BPCL', 'GAIL', 'IOC', 'ONGC', 'Reliance Industries'], 'Power': [
    'NTPC Limited', 'PowerGrid Corporation of India'], 'Mining': ['Coal India'], 'Financial Services': ['Bajaj Finance', 'Bajaj Finserv', 'HDFC'], 'Food Processing': ['Nestle India Ltd'], 'Information Technology': ['HCL Technologies', 'Infosys', 'Tata Consultancy Services', 'Tech Mahindra', 'Wipro'], 'Infrastructure': ['Adani Ports'], 'Media': ['Zee Entertainment Enterprises'], 'Metals': ['Hindalco', 'JSW Steel', 'Tata Steel', 'Vedanta'], 'Pharmaceuticals': ['Cipla', 'Dr Reddy Lab', 'Sun Pharmaceutical'], 'Telecommunication': ['Airtel', 'Infratel']}

sectorList = ['Automobile', 'Banking', 'Financial Services', 'Cement', 'Chemicals', 'Construction', 'Consumer Goods', 'Energy', 'Power',
              'Mining', 'Food Processing', 'Information Technology', 'Infrastructure', 'Media', 'Metals', 'Pharmaceuticals', 'Telecommunication']

stockList = ["Bajaj Auto", "Eicher Motors", "Hero MotoCorp", "Mahindra", "Maruti Suzuki", "Tata Motors", "Axis Bank", "HDFC Bank", "ICICI Bank", "IndusInd Bank", "Kotak Mahindra Bank", "State Bank of India", "Grasim Industries", "UltraTech Cement", "Shree Cement", "United Phosphorus Limited", "Larsen & Toubro", "Asian Paints Ltd", "Hindustan Unilever", "Britannia Industries", "ITC Limited", "Titan Company", "BPCL",
             "GAIL", "IOC", "ONGC", "Reliance Industries", "NTPC Limited", "PowerGrid Corporation of India", "Coal India", "Bajaj Finance", "Bajaj Finserv", "HDFC", "Nestle India Ltd", "HCL Technologies", "Infosys", "Tata Consultancy Services", "Tech Mahindra", "Wipro", "Adani Ports", "Zee Entertainment Enterprises", "Hindalco", "JSW Steel", "Tata Steel", "Vedanta", "Cipla", "Dr Reddy Lab", "Sun Pharmaceutical", "Airtel", "Infratel"]


def getStockFile(index):
    path = "../data/stocks/alphavantage/" + index
    df = pd.read_csv(path, parse_dates=["timestamp"], index_col=["timestamp"])
    return df


def getSymbol(data):
    index = stock_dict[data]
    return (index["symbol"], index["company"], index["sector"])


def getPolarityScore(row, newsPaper):
    raw_file_data = ""
    vader_score = 0

    raw_heading = str(slugify(row[0]))
    raw_news_file = raw_heading[0:120] + "-" + str(slugify(row[2]))
    raw_file_name = "../data/news/" + newsPaper + "/raw/" + raw_news_file + ".txt"
    url = row[1]

    if path.exists(raw_file_name):
        raw_file = open(raw_file_name, "r", encoding="utf8").read()
        raw_file_split = raw_file.split("-------")
        raw_file_heading = raw_file_split[0]
        raw_file_data = raw_file_split[1]
        raw_file_heading = raw_file_heading.replace("--", ",")
        vader_score = vaderParagraph(raw_file_heading, raw_file_data)
        news_data = raw_file_data.replace("\n", "")
        keyWords, keySectors = getKeyWords(news_data)

        return (raw_file_heading, url, vader_score, keyWords, keySectors, row[2])


def getStockPrice(df, date):

    open_val = -1
    perc_change = 0
    close_val = 0
    while open_val < 0:
        try:
            open_val = df.at[date, "open"][0]
            close_val = df.at[date, "close"][0]
            perc_change = round(100 * (close_val - open_val) / open_val, 2)
        except:
            date = addDay(date)
            # return (0, 0, 0, "invalid")
            return (0, "invalid")

    effect = ""
    if perc_change > 0:
        effect = "positive"
    elif perc_change < 0:
        effect = "negative"
    else:
        effect = "neutral"

    # print(perc_change, open_val, close_val, effect)
    # return (perc_change, open_val, close_val, effect)
    return (perc_change, effect)


def addDay(day):
    dt_object = datetime.strptime(day, "%Y-%m-%d")
    date1 = dt_object + timedelta(days=1)
    timestamp = datetime.timestamp(date1)
    date_time = datetime.fromtimestamp(timestamp)
    d = date_time.strftime("%Y-%m-%d")
    return d


def getCsvRows(inputFile, newsPaper, idx_lower, idx_upper):

    relevant_docs = 0
    retrieved_docs = 0
    date_num = 0
    final_dict = dict()
    prints = 0

    inputFileOpen = open(
        "../data/news/" + newsPaper + "/" + inputFile, "r", encoding="utf-8"
    )
    inputFile = csv.reader(inputFileOpen)

    for idx, row in enumerate(inputFile):
        retrieved_docs = retrieved_docs + 1

        if idx < idx_lower:
            continue
        if idx > idx_upper:
            break
        if row[0] == "":
            continue
        if idx % 100 == 0:
            print("{} iterations done".format(idx))
        try:
            (
                headline,
                link,
                vader_score,
                stocks_arr,
                sectors_arr,
                dates,
            ) = getPolarityScore(row, newsPaper)
        except:
            continue

        entered_stock = False

        if stocks_arr != []:
            entered_stock = True
            relevant_docs = relevant_docs + 1

            stocks_arr = stocks_arr.split("|")

            if not dates in final_dict:
                final_dict[dates] = {"sector": {}}
                date_num = date_num + 1
            for stock in stocks_arr:
                if not stock in final_dict[dates]:
                    final_dict[dates][stock] = {
                        "vader": [], "link": [], "headline": []}
                final_dict[dates][stock]["vader"].append(vader_score)
                final_dict[dates][stock]["link"].append(link)
                final_dict[dates][stock]["headline"].append(headline)

            if sectors_arr != [] and sectors_arr != " ":
                sectors_arr = sectors_arr.strip().split("|")
                for sector in sectors_arr:
                    if not sector in final_dict[dates]["sector"]:
                        final_dict[dates]["sector"][sector] = {'vader':[],'link':[], "headline": []}
                    
                    final_dict[dates]["sector"][sector]["vader"].append(vader_score)
                    final_dict[dates]["sector"][sector]["link"].append(link)
                    final_dict[dates]["sector"][sector]["headline"].append(headline)

        if not entered_stock and sectors_arr != []:
            relevant_docs = relevant_docs + 1
            sectors_arr = sectors_arr.strip().split("|")

            if not dates in final_dict:
                final_dict[dates] = {"sector": {}}
                date_num = date_num + 1

            for sector in sectors_arr:
                if not sector in final_dict[dates]["sector"]:
                    final_dict[dates]["sector"][sector] = {'vader':[],'link':[], "headline": []}
                
                final_dict[dates]["sector"][sector]["vader"].append(vader_score)
                final_dict[dates]["sector"][sector]["link"].append(link)
                final_dict[dates]["sector"][sector]["headline"].append(headline)

    return final_dict, relevant_docs, retrieved_docs, date_num


def makeKeyWordList(filename, paper, idx_lower, idx_upper):

    sector_avg_score = {}
    ts = time()

    final_dict, relevant_docs, retrieved_docs, date_num = getCsvRows(
        filename, paper, idx_lower, idx_upper
    )

    if(relevant_docs==0):
        return -2

    tp, tn, fp, fn = 0, 0, 0, 0

    sector_dict = dict()
    stock_assoc_dict = dict()

    # score dict in format: {'date':{'stock':[mean_vader,mean_sector,mean_sector_stock,stock_price]}}
    score_dict = dict()

    for date in final_dict:
        avg_day_score=0
        avg_day_score_idx=0

        score_dict[date] = {}
        stock_assoc_dict[date] = {}

        # Tabulate score for each sector
        if "sector" in final_dict[date]:
            for sectors in final_dict[date]["sector"]:
                if not date in sector_dict:
                    sector_dict[date] = {}
                sector_dict[date][sectors] = round(
                    mean(final_dict[date]["sector"][sectors]["vader"]), 2)

        for sector in sectorList:
            try:
                if sector not in sector_dict[date]:
                    sector_dict[date][sector] = 0
            except:
                sector_dict[date] = {}
                sector_dict[date][sector] = 0

        # Start populating score_dict
        for index in stockList:
            score_dict[date][index] = [
                0, 0, 0, -1, "inavlid", "sector", "symbol","news",date]

            symbol, industry, sector = getSymbol(index.strip())
            perc_change, effect = getStockPrice(getStockFile(symbol), date)

            score_dict[date][index][1] = sector_dict[date][sector]
            score_dict[date][index][3] = perc_change
            score_dict[date][index][4] = effect
            score_dict[date][index][5] = sector
            score_dict[date][index][6] = symbol

            score7 = ""
            if index in final_dict[date]:
                for idx,news_score in enumerate(final_dict[date][index]["vader"]):
                    score7 = score7+ str(news_score)+" : "+final_dict[date][index]["headline"][idx]


            score_dict[date][index][7] = score7

            if index != "sector" and index in final_dict[date]:
                score_dict[date][index][0] = round(
                    mean(final_dict[date][index]["vader"]), 2)

                avg_day_score = avg_day_score+score_dict[date][index][0]
                avg_day_score_idx = avg_day_score_idx+1
            
        if avg_day_score_idx!=0:
            avg_day_score = avg_day_score/avg_day_score_idx

        # Tabluate score for each stock
        for sector in sectorStockDict:
            avg = 0
            avg_number = 0
            for stocks in sectorStockDict[sector]:
                avg = avg + score_dict[date][stocks][0]
                avg_number = avg_number+1
            avg = round(avg/avg_number,2)
            stock_assoc_dict[date][sector] = avg


        for index in stockList:
            score_dict[date][index][2] = stock_assoc_dict[date][score_dict[date][index][5]]

            cR = score_dict[date][index]
            if cR[0] !=0 or cR[4]!="invalid" or cR[4]!="neutral":


                if cR[3] > 0 and cR[0] > 0:
                    tp = tp + 1
                elif cR[3] < 0 and cR[0] < 0:
                    tn = tn + 1
                elif cR[3] < 0 and cR[0] > 0:
                    print(score_dict[date][index])
                    fp = fp + 1
                elif cR[3] > 0 and cR[0] < 0:
                    fn = fn + 1

                # print(date, index, score_dict[date][index])
                
                

    print("\nConfusion matrix: \nTP: {}\tFP: {}\nFN: {}\tTN: {}".format(tp, fp, fn, tn))

    # precision = round((retrieved_docs / (relevant_docs + retrieved_docs)) * 100, 2)
    # recall = round((relevant_docs / (relevant_docs + retrieved_docs)) * 100, 2)

    if (tp + tn + fp + fn) == 0:
        print("Error:",paper,idx_lower,idx_upper)
        for dates in score_dict:
            print(dates)
        # print(score_dict)
        return -1

    try:
        acc = round(((tn + tp) / (tp + tn + fp + fn)) * 100, 4)
    except Exception as e:
        return -2
    # specificity = round((tn / (tn + fp)) * 100, 2)
    # sensitivity = round((tp / (tp + fn)) * 100, 2)

    print("Accuracy = {}%".format(acc))
    # print("Retrieved = {}, Relevant = {}".format(retrieved_docs, relevant_docs))
    # print("Specificity = {}".format(specificity))
    # print("Date Num = {}".format(date_num))

    # print("Took ", time() - ts)
    # print("Sensitivity = {}".format(sensitivity))
    # print("Precision = {}".format(precision))
    # print("Recall = {}".format(recall))

    return acc


def main():
    index, company, sector = getSymbol("Bajaj")
    getStockPrice(getStockFile(index), "2019-07-28")


# makeKeyWordList()
if __name__ == "__main__":
    # getCsvRows('moneyctl-merged-buisness.csv', "moneycontrol")
    # getCsvRows('economic-merged-formatted.csv', "economic")
    # getCsvRows('economic-merged.csv', "economic")
    # getCsvRows('deccan-business.csv', "deccan")
    # getCsvRows('firstpost-merged.csv', "firstpost")

    newspaperList = [
        ["economic-merged.csv", "economic"],
        ["deccan-business.csv", "deccan"],
        ["firstpost-merged.csv", "firstpost"],
        ["moneyctl-merged-buisness.csv", "moneycontrol"],
    ]
    ts = time()

    # results = []
    # gaps = 5000
    # idx_upper = 75000

    # for idxx in range(0, 1):
    #     lists = [
    #         (newspaperList[idxx][0], newspaperList[idxx][1], x, x + gaps)
    #         for x in range(0, idx_upper, gaps)
    #     ]
    #     with multiprocessing.Pool(processes=12) as pool:
    #         results2 = pool.starmap(makeKeyWordList, lists)
    #     results = results + results2

    # res = 0
    # i = 0
    # for result in results:
    #     if result > 0:
    #         res = res + result
    #         i = i + 1

    # print(results, res / i, i)

    # print("Took ", time() - ts)

    # results = makeKeyWordList(
    #     newspaperList[1][0], newspaperList[1][1], 0, 400)
    results = makeKeyWordList(
        'ultimate-merged3.csv', newspaperList[1][1], 0, 400)
    print(results)
