import urllib
import urllib.request
import time
import random


# Stocks lst
stocks_list = ["BAJAJ-AUTO", "EICHERMOT", "HEROMOTOCO", "M%26M", "MARUTI", "TATAMOTORS", "AXISBANK", "HDFCBANK", "ICICIBANK", "INDUSINDBK", "KOTAKBANK", "SBIN", "GRASIM", "ULTRACEMCO", "SHREECEM", "UPL", "LT", "ASIANPAINT", "HINDUNILVR", "BRITANNIA", "ITC", "TITAN", "BPCL", "GAIL",
               "IOC", "ONGC", "RELIANCE", "NTPC", "POWERGRID", "COALINDIA", "BAJFINANCE", "BAJAJFINSV", "HDFC", "NESTLEIND", "HCLTECH", "INFY", "TCS", "TECHM", "WIPRO", "ADANIPORTS", "ZEEL", "HINDALCO", "JSWSTEEL", "TATASTEEL", "VEDL", "CIPLA", "DRREDDY", "SUNPHARMA", "BHARTIARTL", "INFRATEL"]

stocks_list = ["TATAMOTORS"]
# Misc
api_key = ["D4V3YEYJGNXZ27PL", "BEZAPQ60MX6M0MTV", "C73M71O6LA04D9KI",
           "4D5AD7GG5BUJ0R9Y", "5LIB86FZXJJ5YQD3", "LK8JHRNLLTU90Q9C"]
outputsize = "full"


# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE%3A&interval=5min&apikey=demo
# Url initialization

def downloadAllDaily():

    sopped = False
    start_time = time.time()
    end_time = time.time()
    endlist = ""
    lol = 0
    for filename in stocks_list:

        rand_key = api_key[random.randrange(0, len(api_key))]
        #rand_key = api_key[random.choice([0,1,2])]
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NSE%3A" + \
            filename+"&apikey="+rand_key+"&datatype=csv&outputsize="+outputsize

        print(url)

        if(filename == "M%26M"):
            filename = "M&M"

        print("Starting download of {0} using key {1}".format(
            filename, rand_key))
        page = urllib.request.urlopen(url)

        content = page.read()

        # print(content)
        if b'hank you for using Alpha Vantage' not in content:
            print("Yes")

            f = open("../../data/stocks/alphavantage/"+filename, "wb")
            f.write(content)
            f.close()
            if sopped == True:
                elapsed_time = time.time() - start_time
                print(elapsed_time)
                sopped = False

        else:
            endlist += "\",\""+filename
            print("No\nStopping for 30 seconds")

            sopped = True
            if sopped == False:
                start_time = time.time()
            time.sleep(15)
        print(endlist)
        print("Finsihed downloading\n\n")
    # print(endlist)


def downloadIntraDay(stock):
    rand_key = api_key[random.randrange(0, len(api_key))]
    #rand_key = api_key[random.choice([0,1,2])]
    # url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE%3A" + \
    #     stock+"&apikey="+rand_key+"&datatype=csv&interval=5min&outputsize="+outputsize
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NSE&apikey=" + \
        rand_key+"&datatype=csv&outputsize="+outputsize

    print(url)

    print("Starting download of {0} using key {1}".format(
        stock, rand_key))
    page = urllib.request.urlopen(url)

    content = page.read()
    # print(content)
    # f = open("../../data/stocks/alphavantage/"+stock+"-Intra.csv", "wb")
    f = open("../../data/stocks/NSE.csv", "wb")
    f.write(content)
    f.close()


if __name__ == '__main__':
    downloadAllDaily()
    # downloadIntraDay("NSE")
