import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, send_from_directory
import json
import urllib.request
import os
import random
from datetime import date
from nlp.vader_sentiment import vaderParagraph, vaderAtOnce
import re
import os
import csv
import pandas as pd
from nlp.words import getKeyWords
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

stocks = ["3M India","Aavas Financiers","Abbott India","ACC","Adani Enterprises","Adani Gas","Adani Green Energy","Adani Ports and Special Economic Zone","Adani Power","Adani Transmission","Aditya Birla Capital","Aditya Birla Fashion and Retail","Advanced Enzyme Technologies","Aegis Logistics","AIA Engineering","Ajanta Pharma","Akzo Nobel India","Alembic Pharmaceuticals","Alkem Laboratories","Alkyl Amines Chemicals","Allcargo Logistics","Amara Raja Batteries","Amber Enterprises India","Ambuja Cements","APL Apollo Tubes","Apollo Hospitals Enterprise","Apollo Tyres","Arvind Fashions","Ashoka Buildcon","Ashok Leyland","Asian Paints","Aster DM Healthcare","Astral Poly Technik","Astrazeneca Pharma India","Atul","Aurobindo Pharma","AU Small Finance Bank","Avanti Feeds","Avenue Supermarts","Axis Bank","Bajaj Auto Ltd","Bajaj Consumer Care","Bajaj Electricals","Bajaj Finance","Bajaj Finserv","Bajaj Holdings & Investment","Balkrishna Industries","Balmer Lawrie & Co.","Balrampur Chini Mills","Bandhan Bank","Bank Of Baroda","Bank of India","Bank of Maharashtra","BASF India","Bata India","Bayer CropScience","BEML Ltd","Berger Paints India","Bharat Dynamics","Bharat Electronics","Bharat Forge","Bharat Heavy Electricals","Bharat Petroleum Corpn.","Bharti Airtel","Bharti Infratel","Biocon","Birla Corporation","Bliss GVS Pharma","Blue Dart Express","Blue Star","Bombay Burmah Trdg. Corpn.","Bombay Dyeing & Mfg. Co.","Bosch","Brigade Enterprises","Britannia Industries","Cadila Healthcare","Canara Bank","Can Fin Homes","Caplin Point Laboratories","Capri Global Capital","Carborundum Universal","CARE Ratings","Castrol India","CCL Products (India)","Ceat","Central Bank of India","Centrum Capital Limited","Century Plyboards (India)","Cera Sanitaryware","CESC","Chalet Hotel","Chambal Fertilisers & Chemicals","Chennai Petroleum Corpn.","Cholamandalam Financial Holdings","Cholamandalam Investment & Finance Co.","Cipla","City Union Bank","Coal India","Cochin Shipyard","Colgate-Palmolive (India)","Container Corpn. Of India","Coromandel International","CreditAccess Grameen","Crisil","Crompton Greaves Consumer Electricals","Cummins India","Cyient Limited","Dabur India","Dalmia Bharat","DB Corporation","DCB Bank","DCM Shriram","Deepak Fertilisers & Petrochemicals Corpn.","Deepak Nitrite","Delta Corp","Dewan Housing Finance Corpn.","Dhanuka Agritech","Dilip Buildcon","Dishman Carbogen Amcis","Dish TV India","Divi's Laboratories","Dixon Technologies (India)","DLF","Dr. Lal Pathlabs","Dr. Reddy's Laboratories","eClerx Services Ltd","Edelweiss Financial Services","Eicher Motors","EID-Parry (India)","EIH","Emami","Endurance Technologies","Engineers India","Equitas Holdings","Eris Lifesciences Ltd","Esab India","Escorts","Essel Propack","Exide Industries","FDC","Federal Bank","Fine Organic Industries","Finolex Cables","Finolex Industries","Firstsource Solutions","Force Motors","Fortis Healthcare (India) Ltd","Future Consumer","Future Lifestyle Fashion","Future Retail","GAIL (India)","Galaxy Surfactants","Garden Reach Shipbuilders & Engineers","Garware Technical Fibres","Gateway Distriparks","Gayatri Projects","General Insurance Corporation of India","GE Power India","GE T&D India","GHCL","GIC Housing Finance","Gillette India","Glaxosmithkline Pharmaceuticals","Glenmark Pharmaceuticals","GMM Pfaudler","GMR Infrastructure Ltd","Godfrey Phillips India","Godrej Agrovet","Godrej Consumer Products","Godrej Industries","Godrej Properties","Granules India","Graphite India","Grasim Industries","Great Eastern Shipping Company","Greaves Cotton","Grindwell Norton","Gujarat Alkalies & Chemicals","Gujarat Gas","Gujarat Mineral Devp. Corpn.","Gujarat Narmada Valley Fertilizers & Chemicals","Gujarat Pipavav Port Ltd","Gujarat State Fertilizers & Chemicals","Gujarat State Petronet","Gulf Oil Lubricants India","Hathway Cable & Datacom","Havells India","Hawkins Cookers","HCL Technologies","HDFC Asset Management Company","HDFC Bank","HDFC Life Insurance Co","HEG","Heidelberg Cement India","Heritage Foods","Hero Motocorp","Hexaware Technologies","HFCL","Himadri Speciality Chemical","Himatsingka Seide","Hindalco Industries","Hindustan Aeronautics","Hindustan Copper","Hindustan Petroleum Corpn.","Hindustan Unilever","Hindustan Zinc","Honeywell Automation India","Housing Development Finance Corpn.","Housing & Urban Development Corpn.","ICICI Bank","ICICI Lombard General Insurance Company","ICICI Prudential Life Insurance Company","ICICI Securities","IDBI Bank","IDFC First Bank","IDFC","IFB Industries","IFCI","IIFL Finance","Indiabulls Housing Finance","Indiabulls Integrated Services","Indiabulls Real Estate","India Cements","Indian Bank","Indian Energy Exchange","Indian Hotels Co.","Indian Oil Corpn.","Indian Overseas Bank","India Tourism Devp. Corpn.","Indostar Capital Finance Pvt","Indraprastha Gas","Indusind Bank","Infibeam Avenues","Info Edge (India)","Infosys","INOX Leisure","Inox Wind","Intellect Design Arena","Interglobe Aviation","Ipca Laboratories","IRB Infrastructure Developers","Ircon International","ITC","ITD Cementation India","ITI","Jagran Prakashan","Jai Corp","Jain Irrigation Systems","Jammu & Kashmir Bank","Jamna Auto Inds.","JB Chemicals & Pharmaceuticals","Jindal Saw","Jindal Stainless (Hisar)","Jindal Stainless","Jindal Steel & Power","JK Cement Ltd","JK Lakshmi Cement","JK Paper","JK Tyre & Industries","JM Financial","Johnson Controls - Hitachi Air Conditioning India","JSW Energy","JSW Steel","JTEKT India","Jubilant FoodWorks","Jubilant Life Sciences","Just Dial","Jyothy Labs","Kajaria Ceramics","Kalpataru Power Transmission","Kansai Nerolac Paints","Karnataka Bank","KEC International","Kei Industries","KNR Constructions","Kotak Mahindra Bank","KPIT Technologies","KPR Mills","KRBL","KSB","Lakshmi Machine Works","Lakshmi Vilas Bank","La Opala RG","Larsen & Toubro Infotech","Larsen & Toubro","Laurus Labs","Lemon Tree Hotels","LIC Housing Finance","Linde India","L&T Finance Holdings","L&T Technology Services","Lupin","Lux Industries","Mahanagar Gas","Maharashtra Scooters","Maharashtra Seamless","Mahindra CIE Automotive","Mahindra Holidays & Resorts India Ltd","Mahindra Lifespace Developers","Mahindra Logistics","Mahindra & Mahindra Financial Services","Mahindra & Mahindra","Manappuram Finance","Mangalore Refinery & Petrochemicals","Marico","Maruti Suzuki India","Mas Financial Services","Max Financial Services","Max India","Meghmani Organics","Metropolis Healthcare","Minda Corporation","Minda Industries","MindTree","Mishra Dhatu Nigam","MMTC","Moil","Motherson Sumi Systems","Motilal Oswal Financial Services Ltd","Mphasis","MRF","Multi Commodity Exchange India","Muthoot Finance","Narayana Hrudayalaya","Natco Pharma","National Aluminium Co.","National Thermal Power Corp.","Nava Bharat Ventures","Navin Fluorine International","Navneet Education","NBCC India","NCC","Nesco","Nestle India","Network 18 Media & Investments","NHPC","NIIT Technologies","Nilkamal","Nippon Life India Asset Management","NLC India","NMDC","NOCIL","Oberoi Realty","Oil India","Oil & Natural Gas Corpn.","Omaxe","Oracle Financial Services Software","Orient Cement","Orient Electric","Orient Refractories Limited","Page Industries","Parag Milk Foods","PC Jeweller","Persistent Systems","Petronet LNG","Pfizer","Phillips Carbon Black","Phoenix Mills","Pidilite Industries","PI Industries","Piramal Enterprises","PNB Housing Finance","PNC Infratech","Polycab India","Power Finance Corpn.","Power Grid Corporation of India","Prestige Estates Projects","Prism Johnson","Procter & Gamble Health","Procter & Gamble Hygiene & Health Care","PTC India","Punjab National Bank","PVR","Quess Corp","Radico Khaitan","Rail Vikas Nigam","Rain Industries","Rajesh Exports","Rallis India","Rashtriya Chemicals & Fertilizers","Ratnamani Metals & Tubes","Raymond","RBL Bank","REC","Redington India","Relaxo Footwears","Reliance Capital","Reliance Industries","Reliance Infrastructure","Reliance Power","Repco Home Finance","Responsive Industries","Rites","Sadbhav Engineering","Sanofi India","SBI Life Insurance Company","Schaeffler India","Schneider Electric Infrastructure","Security and Intelligence Services (India)","Shankara Building Products","Sheela Foam","Shilpa Medicare","Shipping Corpn. Of India","S H Kelkar and Company Ltd","Shopper's Stop","Shree Cement","Shriram City Union Finance","Shriram Transport Finance Co.","Siemens","SJVN","SKF India","Sobha","Solar Industries India","Somany Ceramics","Sonata Software","South Indian Bank","Spicejet","SRF","Star Cement Ltd","State Bank of India","Steel Authority Of India","Sterlite Technologies","Strides Pharma Science","Sudarshan Chemical Inds.","Sundram Fasteners","Sun Pharma Advanced Research Company","Sun Pharmaceutical Inds.","Sunteck Realty","Sun TV Network","Suprajit Engineering","Supreme Industries","Suzlon Energy","Swan Energy","Symphony","Syngene International","Take Solutions","Tamil Nadu Newsprint & Papers","Tata Coffee","Tata Consultancy Services","Tata Consumer Products","Tata Elxsi","Tata Investment Corpn.","Tata Metaliks","Tata Motors DVR","Tata Motors","Tata Power Co.","Tata Steel","TCI Express","TCNS Clothing Co","TeamLease Services","Tech Mahindra","Tejas Networks","The New India Assurance Co.","The Ramco Cements","Thermax","Thyrocare Technologies","Time Technoplast Ltd","Timken India","Titan Company","Torrent Pharmaceuticals","Torrent Power","Trent","Trident","TTK Prestige","Tube Investments Of India","TV18 Broadcast","TVS Motor Co.","TVS Srichakra","TV Today Network","UCO Bank","UFLEX","Ujjivan Financial Services","Ultratech Cement","Union Bank of India","United Breweries","UPL","Vaibhav Global","Vardhman Textiles","Varroc Engineering Pvt","Varun Beverages","VA Tech Wabag Ltd","Vedanta","Venky's (India)","V-Guard Industries","Vinati Organics","VIP Industries","V-Mart Retail","Vodafone Idea","Voltas","VRL Logistics","VST Industries","Wabco India","Welspun Corp","Welspun India","Westlife Development","Whirlpool Of India","Wipro","Wockhardt","Zee Entertainment Enterprises","Zensar Technologies","Zydus Wellness"]
write_to_file = 0


def getSymbol(data):
    index = stock_dict[data]
    return (index["company"], index["sector"])

def getPolarityScore(row):
    raw_file_data = ""
    vader_score = 0
    url = row[1]
    raw_file_heading = row[0].replace("--", ",")
    vader_score = vaderParagraph(raw_file_heading, raw_file_heading)
    news_data = raw_file_heading.replace("\n", "")
    keyWords, keySectors = getKeyWords(news_data)
    return (raw_file_heading, url, vader_score, keyWords, keySectors, row[2])


def getCsvRows():

    relevant_docs = 0
    retrieved_docs = 0
    date_num = 0
    final_dict = dict()
    prints = 0
    
    today = str(date.today())
    print("Today's date:", today)

    url = "http://192.168.0.122:8080/top-headlines.json"
    response = requests.get(url)
    data = response.json()
    for datas in data["articles"]:
        pubDate = datas["publishedAt"].split("T")[0]

        # if pubDate==today:
        row=[datas["title"],datas["url"],pubDate,datas["source"]["name"]]


        retrieved_docs = retrieved_docs + 1
        (
            headline,
            link,
            vader_score,
            stocks_arr,
            sectors_arr,
            dates,
        ) = getPolarityScore(row)
        # else:
            # vader_score=0

        entered_stock = False

        if stocks_arr != [] and vader_score!=0:
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


def makeKeyWordList():
    output_file = open("./test.csv","a")

    outs = ""
    outs2 = ""
    cr=[0,0,0]

    sector_avg_score = {}
    ts = time()

    final_dict, relevant_docs, retrieved_docs, date_num = getCsvRows()

    if(relevant_docs==0):
        return -3

    tp, tn, fp, fn = 0, 0, 0, 0

    sector_dict = dict()
    stock_assoc_dict = dict()

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
                0, 0, 0, -1, "inavlid", "sector", "symbol","news"]

            industry, sector = getSymbol(index.strip())

            score_dict[date][index][1] = sector_dict[date][sector]
            score_dict[date][index][5] = sector

            score7 = ""
            if index in final_dict[date]:
                for idx,news_score in enumerate(final_dict[date][index]["vader"]):
                    score7 = score7+ str(news_score)+" : "+final_dict[date][index]["headline"][idx].replace("\n","").replace(",","--")+" | "


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
            score = cR[0]

            prediction = cR[3]
            if cR[0]!=0 or cR[1]!=0 or cR[2]!=0:
                outs = outs + str(date)+","+str(index)+","+str(cR)+"\n"

    outs = outs.replace("[","").replace("]","").replace("\"","").replace(", ",",")
    print(outs)
    output_file.close()
                
          
if __name__ == "__main__":
    makeKeyWordList()