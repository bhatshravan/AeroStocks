import requests
from bs4 import BeautifulSoup
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def downloadEconomicAll(curpg):

    links = []
    headlines = []
    date_of_articles = []
    p_content = []
    page = 'https://economictimes.indiatimes.com/lazyloadlistnew.cms?msid=2146843&curpg=' + \
        str(curpg)+'&img=0'
    response = requests.get(page)
    soup = BeautifulSoup(response.content, "html.parser")

    output_file = open("../../data/news/economic/all.csv", "a")

    for anchor in soup.find_all('div', attrs={'class': 'eachStory'}):
        headline = anchor.find('a')
        if("videoshow/" in headline['href']):
            break
        time = anchor.find('time').get_text().replace(",", "-")

        headline_title = headline.get_text().replace(",", "--")
        print(headline['href'])
        print(headline_title)
        print(time)
        outs = str(headline_title)+", " + \
            str(headline['href'])+", " + str(time)+"\n"
        output_file.write(outs)
        print("\n\n")

    output_file.close()


def downloadEconomicOne(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find('div', attrs={'class': 'Normal'})
    news_article = cleanhtml(article.get_text())
    print(news_article)


if __name__ == '__main__':
    # for i in range(1, 100):
    #     downloadEconomicAll(i)
    downloadEconomicOne(
        'https://economictimes.indiatimes.com/markets/stocks/news/cadila-healthcare-gets-eir-from-usfda-for-its-ahmedabad-facility/articleshow/74063201.cms')
