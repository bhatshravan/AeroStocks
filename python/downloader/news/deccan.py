# Imports

import requests
from datetime import timedelta, date
from bs4 import BeautifulSoup
import re

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


def printLinks(currentDate):
    print(currentDate)
    global output_file
    response = requests.post(url, json={'arcDate': currentDate})
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = soup.find_all('h2')
    contents = soup.find_all('ul', {'class': 'group'})

    for idx, content in enumerate(contents):
        contentLinks = content.findChildren('li')
        for contentLink in contentLinks:
            contentList = [normalizeSentence(contentLink.string),
                           contentLink.a['href'], normalizeSpaces(headlines[idx].string), currentDate]
            outs = ','.join(contentList)
            outs = outs+"\n"
            output_file.write(outs)
            hL = headlines[idx].string
            if(hL.startswith("Business")):
                print(contentLink.a['href'])

    # Print all headlines Only
    # for idx, headline in enumerate(headlines):
    #     print(idx, headline.string)


def daterange(d1, d2):
    return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))


def main():
    m1 = m2 = ""
    global output_file
    date1 = date(2020, 1, 1)
    date2 = date(2020, 1, 3)

    for d in daterange(date1, date2):
        m2 = int(d.strftime('%m'))
        y = int(d.strftime('%y'))
        if(m2 != m1):
            m1 = m2
            ops = "../../data/news/deccan/"+str(d.strftime('%Y_%m'))+".csv"
            output_file.close()
            output_file = open(ops, "w")
            output_file.write("headline,link,category,date\n")

        printLinks(d.strftime('%Y/%m/%d'))

    output_file.close()


if __name__ == "__main__":
    main()
