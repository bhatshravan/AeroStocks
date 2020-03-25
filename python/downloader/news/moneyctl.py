import requests
from bs4 import BeautifulSoup
import dates as dts


def downloadMtlAll(url, page):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    i = 0
    b = []
    a = []

    b.append('')
    a.append('')
    output_file = open("../../data/news/moneycontrol/2020.csv", "a")
    for LiIds in range(1, 25):
        LiId = "newslist-"+str(LiIds)

        sp = soup.find('li', {"id": LiId})
        title = sp.find('h2').get_text().replace(
            "\n", "").replace(",", "").strip()
        link = sp.find('a').get('href')
        # date = sp.find('span').get_text().replace(
        #     ", 2020 ", "/2020-").replace(" ", "/")
        date = sp.find('span').get_text()

        outs = str(title)+", "+str(link)+", "+str(date)+"\n"
        print(outs)
        # output_file.write(outs)
    output_file.close()


def downloadMtlUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"class": "artTitle"}).get_text()
    data = ""

    sp = soup.find('div', {"id": "article-main"})
    for p in sp.findAll('p'):
        o = p.get_text()
        if(not o.startswith("Disclaimer")):
            data = data + o.replace("\n", "").replace("\"", "")

    return(title, data)


if __name__ == '__main__':
    for pages in range(1, 200):
        page = "page-"+str(pages)
        a = downloadMtlAll(
            "https://www.moneycontrol.com/news/business/"+page, "news-all-page-1.csv")
# https://www.moneycontrol.com/news/business/
# title, data = downloadUrl(
#     "https://www.moneycontrol.com/news/business/tech-mahindra-q3-pat-may-dip-10-3-qoq-to-rs-1008-cr-motilal-oswal-4792611.html")
# print(title, data)
