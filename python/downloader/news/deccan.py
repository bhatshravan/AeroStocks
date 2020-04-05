# Imports
import requests
from bs4 import BeautifulSoup
import re
import math
from datetime import datetime, timedelta, date
import dates as dts

# Variables
url = "https://www.deccanherald.com/getarchive"


def downloadDeccanOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"id": "page-title"}).get_text()

    contents = soup.find_all('div', {"class": "content"})
    data = ""

    date = soup.find(
        'li', {'class': 'sanspro-semib text-uppercase crud-items__lists'})
    print(dts.deccan(date.get_text().strip()))

    for content in contents:
        data = data + content.get_text()

    # print(title, data)
    return(data)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def downloadDeccanAll(currentDate, file_page):
    try:

        response = requests.post(url, json={'arcDate': currentDate})
        print(url,currentDate)
        soup = BeautifulSoup(response.content, "html.parser")

        headlines = soup.find_all('h2')
        contents = soup.find_all('ul', {'class': 'group'})

        output_file = open("../../data/news/deccan/lists/all-" +
                        str(file_page)+".csv", "a")

        currentDate = currentDate.replace("/", "-")
        for idx, content in enumerate(contents):
            contentLinks = content.findChildren('li')
            for contentLink in contentLinks:
                try:
                    tag = (headlines[idx].string).replace(",", "--")
                    headline = (contentLink.string).strip().replace(",", "--")
                    contentList = [headline,
                                "https://www.deccanherald.com"+contentLink.a['href'], currentDate, currentDate, tag]
                    outs = ','.join(contentList)
                    outs = outs+"\n"
                    output_file.write(outs)
                    # print(outs)
                except:
                    continue

        output_file.close()
    except:
        pp=12

# def main():
#     m1 = m2 = ""
#     date1 = date(2020, 3, 1)
#     date2 = date(2020, 3, 3)

#     current_date = [d.strftime('%Y/%m/%d') for d in (date1 + timedelta(days=i)
#                                                      for i in range((date2 - date1).days + 1))]
#     for d in current_date:
#         downloadDeccanAll(d, "1")


if __name__ == "__main__":
    # main()
    downloadDeccanOne(
        "https://www.deccanherald.com/business/business-news/investors-lose-money-as-fiis-turn-negative-on-india-748235.html")
