import requests
from bs4 import BeautifulSoup
import re
import dates as dts


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def downloadEconomicAll(curpg, file_page):

    page = 'https://economictimes.indiatimes.com/archivelist/starttime-' + \
        str(curpg)+'.cms'
    response = requests.get(page)
    soup = BeautifulSoup(response.content, "html.parser")

    output_file = open("../../data/news/economic/lists/all-" +
                       str(file_page)+".csv", "a")
    pagetext = soup.find('span', attrs={'class': 'pagetext'})

    date = soup.find('td', {'class': 'contentbox5'})
    date = dts.economic2(date.get_text().replace(
        "Archives", "").replace(">", "").strip())

    print(date)

    for headline in pagetext.find_all('li'):

        headline_title = headline.get_text().replace(",", "--")
        link = headline.a['href']

        outs = str(headline_title)+",https://economictimes.indiatimes.com/archivelist/starttime-" + \
            str(link)+"\n"
        # try:
        #     # output_file.write(outs)
        #     print(outs)

        # except:
        #     print("Error")
    output_file.close()


def downloadEconomicOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find('div', attrs={'class': 'Normal'})
    news_article = cleanhtml(article.get_text())
    date = soup.find('div', {'class': 'publish_on'}).get_text().replace(
        "Last Updated: ", "").strip()

    print(dts.economic(date))
    return (news_article)


if __name__ == '__main__':
    # for i in range(43914, 43915):
    for i in range(43914, 43915):
        downloadEconomicAll(i, i)
    # downloadEconomicOne(
    #     'https://economictimes.indiatimes.com/markets/stocks/news/cadila-healthcare-gets-eir-from-usfda-for-its-ahmedabad-facility/articleshow/74063201.cms')
# 43914
# 43647
