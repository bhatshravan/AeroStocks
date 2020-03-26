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
    article = soup.find('div', attrs={'class': 'Normal'})
    data = cleanhtml(article.get_text())
    date = soup.find('div', {'class': 'publish_on'}).get_text().replace(
        "Last Updated: ", "").strip()
    date = dts.economic(date)
    data = data+date
    return (data)


def downloadDeccanOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"id": "page-title"}).get_text()

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


def downloadMtlOne(url):
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
        "Last Updated : ", "").replace('| Source: Moneycontrol.com', "").strip()

    date = dts.moneyctl2(date)

    data = data+date
    return(data)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("\n\n", "\n")
    return cleantext


def downloadRawsAndPolarity(row, newsPaper):

    raw_file_data = ""
    raw_file_heading = ""

    raw_heading = str(slugify(row[0]))
    try:
        raw_news_file = raw_heading[0:120]+"-"+str(slugify(row[2]))
    except:
        raw_news_file = raw_heading+"-"+str(slugify(row[2]))

    raw_file_name = '../data/news/'+newsPaper+'/raw/'+raw_news_file+'.txt'

    # url = newsPaperUrl+row[1]
    # url = url.replace(" ", "")
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

        if(newsPaper == "deccan"):
            raw_file_data = downloadDeccanOne(url)
        elif(newsPaper == "economic"):
            raw_file_data = downloadEconomicOne(url)
        else:
            raw_file_data = downloadMtlOne(url)

        print("URL CALL")
        output_file = open(raw_file_name, "w")
        outs = outs+row[0]+"\n-------\n" + \
            raw_file_data+"\n-------\n"+newsPaper
        output_file.write(outs)
        output_file.close()

    raw_file_heading = raw_file_heading.replace("--", ",")
    vader_score = vaderParagraph(raw_file_data)
    vader_polarity = "Neutral news"

    news_data = raw_file_data.replace("\n", "")
    keyWords = getKeyWords(news_data)

    if(vader_score > 0.05):
        vader_polarity = "Positive news"

    if(vader_score < -0.05):
        vader_polarity = "Negative news"

    print("Heading - {}Score = {} , Type = {} \nKeywords - {}\nLink - {}\n\n".format(
        raw_file_heading, vader_score, vader_polarity, keyWords, url))


def downloadInputFile(inputFile, newsPaper):
    inputFileOpen = open('../data/news/'+inputFile, 'rt')
    inputFile = csv.reader(inputFileOpen)

    for idx, row in enumerate(inputFile):
        if(idx > 0):
            break
        if(row[0] == ""):
            continue

        downloadRawsAndPolarity(row, newsPaper)


if __name__ == "__main__":
    # downloadInputFile('deccan/deccan-business.csv')
    downloadInputFile('test.csv', "economic")
