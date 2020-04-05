import requests
from bs4 import BeautifulSoup
import re
import dates as dts
import merge as merge


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def downloadFirstPostAll(curpg, file_page):
    try:

        page = 'https://www.firstpost.com/category/business/page/'+str(curpg)
        print(page)
        response = requests.get(page)
        soup = BeautifulSoup(response.content, "html.parser")

        output_file = open("../../data/news/firstpost/lists/all-" +
                        str(file_page)+".csv", "a")

        uls = soup.find('ul', {'class': 'articles-list'})

        posts = uls.find_all('li')

        for post in posts:

            link = post.a['href']
            post = post.find('div', {'class': 'info-wrap'})
            headline_title = post.find(
                'p', {'class': 'list-title'}).get_text().replace(",", "--")

            date = post.find('p', {'class': 'text-muted'}).text

            date = dts.firstpost(date)

            outs = headline_title+","+link+","+date+"\n"
            try:
                output_file.write(outs)
                # print(outs)
            except:
                print("Error")
                p22=0
        output_file.close()
    except:
        p=22

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

    print(data+"\n"+date)


# downloadFirstPostAll('2', 1)
# https://www.firstpost.com/category/business/page/2
# downloadFirstPostOne(
#     "https://www.firstpost.com/business/finance-ministry-writes-to-rbi-on-coronavirus-relief-measures-asks-central-bank-to-help-borrowers-cope-with-damage-from-outbreak-8193211.html")
