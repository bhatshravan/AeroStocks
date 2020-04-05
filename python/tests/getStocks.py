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

# dc = list()
dc = dict()
for company in stock_dict:
    sector = stock_dict[company]["sector"]
    if not sector in dc:
        dc[sector] = []
        # dc.append(sector)
        # print(sector)
    dc[sector].append(company)

print(dc)
