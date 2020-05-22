import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, send_from_directory
import json
import urllib.request
import os
import random
from datetime import date
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import os
import csv
import pandas as pd
import csv
from slugify import slugify
from datetime import datetime, timedelta, date
import logging
import os.path
from os import path
from statistics import mean
import random
from time import time
import multiprocessing
import sys
# import tensorflow as tf
import json

sectorListMain = ["Automobile", "Chemical", "Communication", "Cons Durable", "Construction", "Diversified", "Energy", "Engineering", "Financial",
                  "FMCG", "Food delivery", "Healthcare", "market", "Metals", "Pharmaceuticals", "Services", "Technology", "Telecommunication", "Textiles", "Transport"]

# Get all companies
companies = []
with open('./companies.txt') as f:
    companies = f.read().splitlines()

# Get all sectors
sectors = []
with open('./sectors.txt') as f:
    sectors = f.read().splitlines()

# model = tf.keras.models.load_model('../classifier/models/model2.h5')


# Returns a sentiment score
def vaderParagraph(data):
    analyzer = SentimentIntensityAnalyzer()
    sentence_list = tokenize.sent_tokenize(data)
    paragraphSentiments = 0.0
    for sentence in sentence_list:
        vs = analyzer.polarity_scores(sentence)
        paragraphSentiments += vs["compound"]
    pos_words = ["rally", "rallies"]
    neg_words = ["plunge up to", "share price falls", "shares fall", "shares dip", "stock plunges", "profit plunges", "drops over", "plummets"
                 "52-week low", "nosedives", "share price tanks", "-yr low", "slides", "dips", "lead fall", "revenue falls"]
    spec_words = ["Buzzing stocks", "ideas from experts"]
    averageSentiment = round(paragraphSentiments / len(sentence_list), 4)
    data = data.lower()
    for words in spec_words:
        if words in data:
            return(0)
    for words in neg_words:
        if words in data:
            if(averageSentiment > 0):
                averageSentiment = -1*averageSentiment
            if(averageSentiment == 0.0):
                averageSentiment = -0.3
            return(averageSentiment)
    for words in pos_words:
        if words in data:
            if(averageSentiment < 0):
                averageSentiment = -1*averageSentiment
            if(averageSentiment == 0.0):
                averageSentiment = 0.3
            return(averageSentiment)
    return ((averageSentiment))


def getKeyWords(data):
    data = data.lower()
    companyList = []
    sectorList = []

    for idx, company in enumerate(companies):
        if company.lower() in data:
            companyList.append([company, sectors[idx]])

    for sector in sectorListMain:
        if sector.lower() in data:
            sectorList.append([sector])

    return(companyList, sectorList)


def main():
    today = str(date.today())
    print("Today's date:", today)

    company_dict = {}
    assoc_dict = {}
    sector_dict = {}
    company_dict_final = {}
    assoc_dict_final = {}
    sector_dict_final = {}

    url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=45bb840c98934815a19ec6784fc50a19&category=business&pageSize=70"
    response = requests.get(url)
    data = response.json()

    rows = []

    for datas in data["articles"]:
        pubDate = datas["publishedAt"].split("T")[0]

        # if pubDate==today:
        row = [datas["title"], datas["url"], pubDate, datas["source"]["name"]]

        headline = datas["title"]
        vaderScore = vaderParagraph(headline)
        headlineCompanies, headlineSector = getKeyWords(headline)

        rows.append([headline, datas["url"], pubDate,
                     headlineCompanies, vaderScore])
        # print("{0}  -  {1} - {2} - {3}".format(headline,vaderScore,headlineCompanies,headlineSector))

        for companyRetrieved in headlineCompanies:
            if companyRetrieved[0] in company_dict:
                company_dict[companyRetrieved[0]].append(vaderScore)
            else:
                company_dict[companyRetrieved[0]] = [vaderScore]

            if companyRetrieved[1] in assoc_dict:
                assoc_dict[companyRetrieved[1]].append(vaderScore)
            else:
                assoc_dict[companyRetrieved[1]] = [vaderScore]

        for companyRetrieved in headlineSector:
            if companyRetrieved[0] in sector_dict:
                sector_dict[companyRetrieved[0]].append(vaderScore)
            else:
                sector_dict[companyRetrieved[0]] = [vaderScore]

    for sectors in sector_dict:
        sector_dict_final[sectors] = round(mean(sector_dict[sectors]), 2)

    for sectors in company_dict:
        company_dict_final[sectors] = round(mean(company_dict[sectors]), 2)

    for sectors in assoc_dict:
        assoc_dict_final[sectors] = round(mean(assoc_dict[sectors]), 2)

    # print("Sector: ", sector_dict_final)
    # print("Company: ", company_dict_final)
    # print("Assoc: ", assoc_dict_final)

    jsonData = {"news": []}

    for row in rows:
        x = {
            "headline": row[0],
            "url": row[1],
            "date": row[2],
            "vader": row[4],
            "prediction": "none"
        }
        if len(row[3]) < 1:
            continue

        else:
            sector_score = 0.0
            assoc_score = float(assoc_dict_final[row[3][0][1]])
            company_score = float(company_dict_final[row[3][0][0]])

            if(row[3][0][1] in sector_dict_final):
                sector_score = sector_dict_final[row[3][0][1]]

            predictions = 0.0
            # predictions = round((model.predict(
            #     [[float(company_score), float(sector_score), float(assoc_score)]])[0][0])*1, 2)
            if(predictions == 0.0 or predictions == -0.0):
                predictions = row[4]

            x["prediction"] = {
                "score": predictions,
                "company": row[3][0][0],
                "sector": row[3][0][1]
            }
            # print(row[0], " - Vader: ", row[3][0][0],
            #       " - Prediction:", (predictions*10))
        jsonData["news"].append(x)
    print(json.dumps(jsonData))


main()
# print(companies, sectors)
