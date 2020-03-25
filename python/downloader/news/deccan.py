# Imports
import requests
from bs4 import BeautifulSoup
import re
import math
from datetime import datetime, timedelta, date

# Variables
url = "https://www.deccanherald.com/getarchive"

global output_file
output_file = open("../test", "a")


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def normalizeSpaces(input):
    return input.strip().replace(" ", "-").lower()


def normalizeSentence(input):
    return re.sub(r'[\'\,\:\/\\\(\)]', '', input.strip().lower())
    # return re.sub(r'[\,]', '--', input.strip())


def printLinks(currentDate):
    print(currentDate)
    global output_file
    response = requests.post(url, json={'arcDate': currentDate})
    soup = BeautifulSoup(response.content, "html.parser")
    print(response.content)

    headlines = soup.find_all('h2')
    contents = soup.find_all('ul', {'class': 'group'})

    for idx, content in enumerate(contents):
        contentLinks = content.findChildren('li')
        for contentLink in contentLinks:
            contentList = [normalizeSentence(contentLink.string),
                           contentLink.a['href'], normalizeSpaces(headlines[idx].string), currentDate]
            # contentList = [normalizeSentence(contentLink.string),
            #                contentLink.a['href'], currentDate, normalizeSpaces(headlines[idx].string)]
            hL = headlines[idx].string
            if(hL.startswith("Business")):
                outs = ','.join(contentList)
                outs = outs+"\n"
                output_file.write(outs)
                print(contentLink.a['href'])

    # Print all headlines Only
    # for idx, headline in enumerate(headlines):
    #     print(idx, headline.string)


def daterange(d1, d2):
    return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))


# Variables
url = "https://www.deccanherald.com/business/business-news/private-sector-salaries-show-slowest-growth-in-10-years-755915.html"
initalUrl = "https://www.deccanherald.com"


def extractUrl(url):
    return(re.findall("\(|\)|\d{6}|\(|\)|\d{5}", url))


def downloadDeccanOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"id": "page-title"}).get_text()

    contents = soup.find_all('div', {"class": "content"})
    data = ""
    for content in contents:
        data = data + content.get_text().replace("\n", "").replace("\"", "")

    print(title)
    print(data)


# downloadUrl(url)


def main():
    m1 = m2 = ""
    global output_file
    date1 = date(2020, 3, 1)
    date2 = date(2020, 3, 7)

    for d in daterange(date1, date2):
        m2 = int(d.strftime('%m'))
        y = int(d.strftime('%y'))
        if(m2 != m1):
            m1 = m2
            ops = "../../data/news/deccan/"+str(d.strftime('%Y_%m'))+".csv"
            # ops = "../../data/news/deccan/all.csv"
            output_file.close()
            output_file = open(ops, "a")
            # output_file = open(ops, "a")
            output_file.write("headline,link,category,date\n")

        printLinks(d.strftime('%Y/%m/%d'))

    output_file.close()


if __name__ == "__main__":
    main()
