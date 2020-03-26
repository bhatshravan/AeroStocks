import requests
from bs4 import BeautifulSoup
import re
from vader_sentiment import vaderParagraph, vaderAtOnce
from words import getKeyWords
import csv
from slugify import slugify
import os.path
from os import path


inputFileOpen = open('../data/news/deccan/2020_03.csv', 'rt')
inputFile = csv.reader(inputFileOpen)

global raw_file_data, raw_file_heading


def downloadEconomicOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find('div', attrs={'class': 'Normal'})
    news_article = cleanhtml(article.get_text())
    return (news_article)


def downloadDeccanOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"id": "page-title"}).get_text()

    contents = soup.find_all('div', {"class": "content"})
    data = ""
    for content in contents:
        data = data + content.get_text()

    return(data)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("\n\n", "\n")
    return cleantext


for idx, row in enumerate(inputFile):
    if(idx > 100):
        break
    if(row[0] == ""):
        continue

    raw_heading = str(slugify(row[0]))
    raw_news_file = raw_heading[0:120]+str(slugify(row[2]))

    raw_file_name = '../data/news/deccan/raw/'+raw_news_file+'.txt'

    url = 'https://www.deccanherald.com'+row[1]
    url = url.replace(" ", "")

    if(path.exists(raw_file_name)):
        raw_file = open(raw_file_name, "r").read()
        raw_file_split = raw_file.split("-------")
        raw_file_heading = raw_file_split[0]
        raw_file_data = raw_file_split[1]

    else:
        outs = ""

        raw_file_heading = row[0]
        raw_file_heading = raw_file_heading.replace("--", ",")

        raw_file_data = downloadDeccanOne(url)

        print("URL CALL")

        output_file = open(raw_file_name, "w")
        outs = outs+row[0]+"\n-------\n"+raw_file_data
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
