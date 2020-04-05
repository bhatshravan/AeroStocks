import requests
from bs4 import BeautifulSoup
import re
from vader_sentiment import vaderParagraph, vaderAtOnce
from words import getKeyWords
import csv
from slugify import slugify
import os.path
from os import path
import dates as dts


def downloadEconomicOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find(
        'div', attrs={'class': 'Normal'})
    data = cleanhtml(article.get_text())

    dataArr = data.split("\n")
    ends = 0
    data = ""
    for idx, row in enumerate(dataArr):
        if "var totalpage" in row:
            ends = idx
            break
        data = data+row+"\n"

    date = soup.find('div', {'class': 'publish_on'}).get_text().replace(
        "Last Updated: ", "").strip()
    date = dts.economic(date)
    data = data+date
    return (data)


def downloadDeccanOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = ""
    try:
        title = soup.find('h1', {"id": "page-title"}).get_text()
    except:
        title = str(soup.find('h1', {"id": "page-title"}))

    title = (cleanhtml(title))

    contents = soup.find_all('div', {"class": "content"})
    data = ""
    for content in contents:
        data = data + content.get_text()

    date = soup.find(
        'li', {'class': 'sanspro-semib text-uppercase crud-items__lists'})

    date = (dts.deccan(date.get_text().strip()))

    # print(title)
    data = data+date
    return(data)


def downloadFirstPostOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    article_arr = soup.find(
        'div', attrs={'class': 'article-full-content'}).find_all('p')

    article = ""

    for p in article_arr:
        article = article+p.text+"\n"

    news_article = cleanhtml(article)

    dataArr = news_article.split("\n")

    ends = 0
    data = ""
    for idx, row in enumerate(dataArr):
        if "var width" in row:
            ends = idx
            break
        data = data+row+"\n"

    date = soup.find('span', {'class': 'article-date'}).get_text().strip()

    date = (dts.firstpost2(date))

    return(data+date)


def downloadMtlOne(url, date1, date2):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"class": "artTitle"}).get_text()
    data = ""

    sp = soup.find('div', {"id": "article-main"})

    for p in sp.findAll('p'):
        o = p.get_text()
        if(not o.startswith("Disclaimer")):
            data = data + o.replace("\n", "").replace("\"", "")

    date = soup.find('div', {'class': 'arttidate'}).get_text().replace(
        "Last Updated : ", "").replace('| Source: Moneycontrol.com', "").replace(" Source: PTI", "").strip()

    sep = "\n-------\n"
    date = sep+date1+sep+date2

    data = data+date

    return(data)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("\n\n", "\n")
    return cleantext


global n
global p
global e
n, p, e = 0, 0, 0


def downloadRawsAndPolarity(row, newsPaper):

    raw_file_data = ""
    raw_file_heading = ""
    vader_score = 0

    raw_heading = str(slugify(row[0]))
    try:
        raw_news_file = raw_heading[0:120]+"-"+str(slugify(row[2]))
    except:
        raw_news_file = raw_heading+"-"+str(slugify(row[2]))

    raw_file_name = '../data/news/'+newsPaper+'/raw/'+raw_news_file+'.txt'

    url = row[1]

    if(path.exists(raw_file_name)):
        raw_file = open(raw_file_name, "r").read()
        raw_file_split = raw_file.split("-------")
        raw_file_heading = raw_file_split[0]
        raw_file_data = raw_file_split[1]

    else:
        outs = ""
        raw_file_heading = row[0]
        raw_file_heading = raw_file_heading.replace("--", ",")

        try:
            if(newsPaper == "deccan"):
                raw_file_data = downloadDeccanOne(url)
            elif(newsPaper == "economic"):
                raw_file_data = downloadEconomicOne(url)
            elif(newsPaper == "firstpost"):
                raw_file_data = downloadFirstPostOne(url)
            else:
                raw_file_data = downloadMtlOne(url, row[2], row[3])

            print("URL CALL:", url)

            output_file = open(raw_file_name, "w")
            outs = outs+row[0]+"\n-------\n" + \
                raw_file_data+"\n-------\n"+newsPaper

            output_file.write(outs)
            output_file.close()
        except Exception as e:
            print("Error: ", url, e)


def downloadInputFile(inputFile, newsPaper):
    inputFileOpen = open('../data/news/'+newsPaper+"/"+inputFile, 'rt')
    inputFile = csv.reader(inputFileOpen)

    prints = 0

    for idx, row in enumerate(inputFile):
        if(idx > 900):
            break
        # if(prints >= 100):
        #     prints = 0
        #     print("Positive:{}, Negative:{}, Neutral:{}, Total={}".format(
        #         p, n, e, (p+n+e)))
        if(row[0] == ""):
            continue
        prints = prints+1
        downloadRawsAndPolarity(row, newsPaper)
        # getPolarityScore(row, newsPaper)

    print("Positive:{}, Negative:{}, Neutral:{}, Total={}".format(p, n, e, (p+n+e)))


def getPolarityScore(row, newsPaper):
    global n
    global p
    global e
    raw_file_data = ""
    vader_score = 0
    raw_heading = str(slugify(row[0]))

    try:
        raw_news_file = raw_heading[0:120]+"-"+str(slugify(row[2]))
    except:
        raw_news_file = raw_heading+"-"+str(slugify(row[2]))

    raw_file_name = '../data/news/'+newsPaper+'/raw/'+raw_news_file+'.txt'

    url = row[1]

    if(path.exists(raw_file_name)):
        try:
            raw_file = open(raw_file_name, "r").read()
            raw_file_split = raw_file.split("-------")
            raw_file_heading = raw_file_split[0]
            raw_file_data = raw_file_split[1]

            raw_file_heading = raw_file_heading.replace("--", ",")
            vader_score = vaderParagraph(raw_file_data)

            vader_polarity = "Neutral news"

            news_data = raw_file_data.replace("\n", "")
            keyWords = getKeyWords(news_data)

            if(keyWords != ""):
                if(vader_score > 0.05):
                    vader_polarity = "Positive news"
                    p = p+1

                elif(vader_score < -0.05):
                    vader_polarity = "Negative news"
                    n = n+1
                else:
                    e = e+1

                # print("Heading - {}Score = {} , Type = {} \nKeywords - {}\nLink - {}\nDate-{}\n\n".format(
                #     raw_file_heading, vader_score, vader_polarity, keyWords, url, row[2]))
                if ((n % 5) == 0):
                    print("Heading - {}Score = {} , Type = {}, Link = {}\nKeywords - {}\n".format(
                        raw_file_heading, vader_score, vader_polarity, url, keyWords))
        except:
            u = 0


# downloadEconomicOne(
#     'https://economictimes.indiatimes.com/archivelist/starttime-/magazines/panache/whatsapp-launches-dark-mode-for-all-users/articleshow/74465519.cms')


# downloadMtlOne('https://www.moneycontrol.com/news/business/co-working-space-rentals-in-pune-33-lower-than-traditional-offices-gurugram-cost-advantage-only-6-5035601.html')
# downloadDeccanOne(
#     'https://www.deccanherald.com/business/economy-business/disaster-management-crucial-in-a-growing-economy-shah-790826.html')
# downloadInputFile('economic-merged.csv', "economic")
# if __name__ == "__main__":
# downloadInputFile('moneyctl-merged-buisness.csv', "moneycontrol")
# downloadInputFile('deccan-business.csv', "deccan")
