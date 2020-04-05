# from vader_sentiment import vaderAtOnce
import urllib
import requests
import time

data_list = ["Bajaj Auto", "Eicher Motors", "Hero MotoCorp", "Mahindra", "Maruti Suzuki", "Tata Motors", "Axis Bank", "HDFC Bank", "ICICI Bank", "IndusInd Bank", "Kotak Mahindra Bank", "State Bank of India", "Grasim Industries", "UltraTech Cement", "Shree Cement", "United Phosphorus Limited", "Larsen & Toubro", "Asian Paints Ltd", "Hindustan Unilever", "Britannia Industries", "ITC Limited", "Titan Company", "BPCL", "GAIL", "IOC",
             "ONGC", "Reliance Industries", "NTPC Limited", "PowerGrid Corporation of India", "Coal India", "Bajaj Finance", "Bajaj Finserv", "HDFC", "Nestle India Ltd", "HCL Technologies", "Infosys", "Tata Consultancy Services", "Tech Mahindra", "Wipro", "Adani Ports", "Zee Entertainment Enterprises", "Hindalco", "JSW Steel", "Tata Steel", "Vedanta", "Cipla", "Dr Reddy Lab", "Sun Pharmaceutical", "Airtel", "Infratel"]

data_list_custom = ["Bajaj", "Eicher", "Hero MotoCorp", "Mahindra", "Maruti", "Tata Motors", "Axis Bank", "HDFC", "ICICI", "IndusInd", "Kotak Mahindra", "State Bank of India", "Grasim", "UltraTech", "Shree", "United Phosphorus", "Larsen & Toubro", "Asian Paints", "Hindustan Unilever", "Britannia", " ITC ", "Titan", "BPCL",
                    "GAIL", "IOC", "ONGC", "Reliance", "NTPC", "PowerGrid Corporation of India", "Coal India", "Bajaj Finance", "Bajaj Finserv", "HDFC", "Nestle India Ltd", "HCL", "Infosys", "Tata Consultancy Services", "Tech Mahindra", "Wipro", "Adani", "Zee", "Hindalco", "JSW", "Tata Steel", "Vedanta", "Cipla", "Dr Reddy", "Sun Pharmaceutical", "Airtel", "Infratel"]

data_list_custom_lower = ['bajaj', 'eicher', 'hero motocorp', 'mahindra', 'maruti', 'tata motors', 'axis bank', 'hdfc', 'icici', 'indusind', 'kotak mahindra', 'state bank of india', 'grasim', 'ultratech', 'shree', 'united phosphorus', 'larsen & toubro', 'asian Zpaints', 'hindustan unilever', 'britannia', ' itc ', 'titan', 'bpcl', 'gail', 'ioc',
                          'ongc', 'Reliance', 'ntpc', 'powergrid corporation of india', 'coal india', 'bajaj finance', 'bajaj finserv', 'hdfc', 'nestle india ltd', 'hcl', 'infosys', 'tata consultancy services', 'tech mahindra', 'wipro', 'adani', 'zee', 'hindalco', 'jsw', 'tata steel', 'vedanta', 'cipla', 'dr reddy', 'sun pharmaceutical', 'airtel', 'infratel']

sector_list = ["Automobile", "Automobile", "Automobile", "Automobile", "Automobile", "Automobile", "Banking", "Banking", "Banking", "Banking", "Banking", "Banking", "Cement shares", "Cement shares", "Cement shares", "Chemicals", "Construction", "Consumer Goods", "Consumer Goods", "Consumer Goods", "Consumer Goods", "Consumer Goods", "Energy", "Energy", "Energy", "Energy", "Energy", "Power", "Power", "Mining",
               "Financial Services", "Financial Services", "Financial Services", "Food Processing", "Information Technology", "Information Technology", "Information Technology", "Information Technology", "Information Technology", "Infrastructure", "Media & Entertainment", "Metals", "Metals", "Metals", "Metals", "Pharmaceuticals", "Pharmaceuticals", "Pharmaceuticals", "Telecommunication", "Telecommunication"]

stock_list = ["BAJAJ-AUTO", "EICHERMOT", "HEROMOTOCO", "M&M", "MARUTI", "TATAMOTORS", "AXISBANK", "HDFCBANK", "ICICIBANK", "INDUSINDBK", "KOTAKBANK", "SBIN", "GRASIM", "ULTRACEMCO", "SHREECEM", "UPL", "LT", "ASIANPAINT", "HINDUNILVR", "BRITANNIA", "ITC", "TITAN", "BPCL", "GAIL",
              "IOC", "ONGC", "RELIANCE", "NTPC", "POWERGRID", "COALINDIA", "BAJFINANCE", "BAJAJFINSV", "HDFC", "NESTLEIND", "HCLTECH", "INFY", "TCS", "TECHM", "WIPRO", "ADANIPORTS", "ZEEL", "HINDALCO", "JSWSTEEL", "TATASTEEL", "VEDL", "CIPLA", "DRREDDY", "SUNPHARMA", "BHARTIARTL", "INFRATEL"]

inputData = "Hello world in mahindra bajaj gail"


def getKeyWords(inputData):
    stocks = []
    companies = []
    sector = []

    inputData = inputData.lower().strip().replace(
        "TCS", "Tata Consultancy Services")

    for idx, word in enumerate(data_list_custom):
        if (word.lower() in inputData):
            if word not in stocks:
                stocks.append(word)

    for idx, word in enumerate(sector_list):
        if (word.lower() in inputData.lower()):
            if word not in sector:
                sector.append(word)
                # print(word)

    stocks_arr = []
    sector_arr = []
    if stocks != []:
        stocks_arr = ("|".join(stocks))
    if sector != []:
        sector_arr = ("|".join(sector))

    return(stocks_arr, sector_arr)


# print(data_list_custom+data_list_custom_lower)


# print(getKeyWords(inputData))
# vaderAtOnce("he compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate")
