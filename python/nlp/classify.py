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
    "Bajaj": {"company": "Bajaj", "symbol": "BAJAJ-AUTO", "sector": "Automobile"},
    "Eicher": {"company": "Eicher", "symbol": "EICHERMOT", "sector": "Automobile"},
    "Hero": {"company": "Hero", "symbol": "HEROMOTOCO", "sector": "Automobile"},
    "Mahindra": {"company": "Mahindra", "symbol": "M&M", "sector": "Automobile"},
    "Maruti": {"company": "Maruti", "symbol": "MARUTI", "sector": "Automobile"},
    "Tata Motors": {
        "company": "Tata Motors",
        "symbol": "TATAMOTORS",
        "sector": "Automobile",
    },
    "Axis Bank": {"company": "Axis Bank", "symbol": "AXISBANK", "sector": "Banking"},
    "HDFC": {"company": "HDFC", "symbol": "HDFCBANK", "sector": "Banking"},
    "ICICI": {"company": "ICICI", "symbol": "ICICIBANK", "sector": "Banking"},
    "IndusInd": {"company": "IndusInd", "symbol": "INDUSINDBK", "sector": "Banking"},
    "Kotak Mahindra": {
        "company": "Kotak Mahindra",
        "symbol": "KOTAKBANK",
        "sector": "Banking",
    },
    "State Bank of India": {
        "company": "State Bank of India",
        "symbol": "SBIN",
        "sector": "Banking",
    },
    "Grasim": {"company": "Grasim", "symbol": "GRASIM", "sector": "Cement"},
    "UltraTech": {"company": "UltraTech", "symbol": "ULTRACEMCO", "sector": "Cement"},
    "Shree": {"company": "Shree", "symbol": "SHREECEM", "sector": "Cement"},
    "United Phosphorus": {
        "company": "United Phosphorus",
        "symbol": "UPL",
        "sector": "Chemicals",
    },
    "Larsen & Toubro": {
        "company": "Larsen & Toubro",
        "symbol": "LT",
        "sector": "Construction",
    },
    "Asian Paints": {
        "company": "Asian Paints",
        "symbol": "ASIANPAINT",
        "sector": "Consumer Goods",
    },
    "Hindustan Unilever": {
        "company": "Hindustan Unilever",
        "symbol": "HINDUNILVR",
        "sector": "Consumer Goods",
    },
    "Britannia": {
        "company": "Britannia",
        "symbol": "BRITANNIA",
        "sector": "Consumer Goods",
    },
    "ITC": {"company": "ITC", "symbol": "ITC", "sector": "Consumer Goods"},
    "Titan": {"company": "Titan", "symbol": "TITAN", "sector": "Consumer Goods"},
    "BPCL": {"company": "BPCL", "symbol": "BPCL", "sector": "Energy"},
    "GAIL": {"company": "GAIL", "symbol": "GAIL", "sector": "Energy"},
    "IOC": {"company": "IOC", "symbol": "IOC", "sector": "Energy"},
    "ONGC": {"company": "ONGC", "symbol": "ONGC", "sector": "Energy"},
    "Reliance": {"company": "Reliance", "symbol": "RELIANCE", "sector": "Energy"},
    "NTPC": {"company": "NTPC", "symbol": "NTPC", "sector": "Power"},
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
    "HCL": {"company": "HCL", "symbol": "HCLTECH", "sector": "Information Technology"},
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
    "Adani": {"company": "Adani", "symbol": "ADANIPORTS", "sector": "Infrastructure"},
    "Zee": {"company": "Zee", "symbol": "ZEEL", "sector": "Media"},
    "Hindalco": {"company": "Hindalco", "symbol": "HINDALCO", "sector": "Metals"},
    "JSW": {"company": "JSW", "symbol": "JSWSTEEL", "sector": "Metals"},
    "Tata Steel": {"company": "Tata Steel", "symbol": "TATASTEEL", "sector": "Metals"},
    "Vedanta": {"company": "Vedanta", "symbol": "VEDL", "sector": "Metals"},
    "Cipla": {"company": "Cipla", "symbol": "CIPLA", "sector": "Pharmaceuticals"},
    "Dr Reddy": {
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
            return (0, 0, 0, "invalid")

    effect = ""
    if perc_change > 0:
        effect = "Positive"
    elif perc_change < 0:
        effect = "Negative"
    else:
        effect = "Neutral"

    # print(perc_change, open_val, close_val, effect)
    return (perc_change, open_val, close_val, effect)


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
                        final_dict[dates]["sector"][sector] = []
                    final_dict[dates]["sector"][sector].append(vader_score)

        if not entered_stock and sectors_arr != []:
            relevant_docs = relevant_docs + 1
            sectors_arr = sectors_arr.strip().split("|")

            if not dates in final_dict:
                final_dict[dates] = {"sector": {}}
                date_num = date_num + 1

            for sector in sectors_arr:
                if not sector in final_dict[dates]["sector"]:
                    final_dict[dates]["sector"][sector] = []
                final_dict[dates]["sector"][sector].append(vader_score)

    return final_dict, relevant_docs, retrieved_docs, date_num


# def makeKeyWordList(filename, newspaper, idx_lower, idx_upper):


def makeKeyWordList(filename, paper, idx_lower, idx_upper):

    sector_avg_score = {}
    ts = time()

    final_dict, relevant_docs, retrieved_docs, date_num = getCsvRows(
        filename, paper, idx_lower, idx_upper
    )

    tp, tn, fp, fn = 0, 0, 0, 0

    for dates in final_dict:
        for index in final_dict[dates]:
            if index == "sector":
                for sectors in final_dict[dates]["sector"]:
                    sector_avg_score = round(
                        mean(final_dict[dates]["sector"][sectors]), 2
                    )
                    # print("{} - {}".format(sectors, sector_avg_score))
            else:
                stock_avg_score = round(
                    mean(final_dict[dates][index]["vader"]), 2)

                symbol, industry, sector = getSymbol(index.strip())
                perc_change, open_val, close_val, effect = getStockPrice(
                    getStockFile(symbol), dates
                )

                if effect == "invalid":
                    continue

                if perc_change > 0 and stock_avg_score > 0:
                    tp = tp + 1
                elif perc_change < 0 and stock_avg_score < 0:
                    tn = tn + 1
                elif perc_change < 0 and stock_avg_score > 0:
                    fp = fp + 1
                    for ids, heads in enumerate(final_dict[dates][index]["headline"]):
                        print(
                            final_dict[dates][index]["headline"][ids],
                            " - ",
                            final_dict[dates][index]["vader"][ids],
                            index,
                        )
                    # print(
                    #     "\nIndex = {}\nVader = {} \t Stock_Change = {}\nHeadline = {} ".format(
                    #         index,
                    #         stock_avg_score,
                    #         perc_change,
                    #         final_dict[dates][index]["headline"],
                    #     )
                    # )

                elif perc_change > 0 and stock_avg_score < 0:
                    fn = fn + 1

    print("\nConfusion matrix: \nTP: {}\tFP: {}\nFN: {}\tTN: {}".format(tp, fp, fn, tn))

    # precision = round((retrieved_docs / (relevant_docs + retrieved_docs)) * 100, 2)
    # recall = round((relevant_docs / (relevant_docs + retrieved_docs)) * 100, 2)

    if (tp + tn + fp + fn) == 0:
        return -1

    try:
        acc = round(((tn + tp) / (tp + tn + fp + fn)) * 100, 4)
    except:
        return -1
    # specificity = round((tn / (tn + fp)) * 100, 2)
    # sensitivity = round((tp / (tp + fn)) * 100, 2)

    # print("Accuracy = {}%".format(acc))
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

    results = []
    gaps = 100
    idx_upper = 100

    for idxx in range(0, 1):

        lists = [
            (newspaperList[idxx][0], newspaperList[idxx][1], x, x + gaps)
            for x in range(0, idx_upper, gaps)
        ]

        with multiprocessing.Pool(processes=1) as pool:
            results2 = pool.starmap(makeKeyWordList, lists)

        # print(newspaperList[idxx][1], " - ", results2)

        results = results + results2

    res = 0
    i = 0
    for result in results:
        if result != -1:
            res = res + result
            i = i + 1

    print(results, res / i, i)

    print("Took ", time() - ts)

    # print(newspaperList[0][0])
    # results = makeKeyWordList(newspaperList[2][0], newspaperList[2][1], 0, 1000)
    # print(results)
