import requests
from bs4 import BeautifulSoup
import dates as dts
import sys

global error
error = 0


def downloadMtlAll(url, page):
    try:
        global error
        url = "https://www.moneycontrol.com/news/business/page-"+str(url)
        # print("------\n", url, "--------\n")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        i = 0
        b = []
        a = []

        b.append('')
        a.append('')
        output_file = open(
            "../../data/news/moneycontrol/lists/mixed-"+str(page)+".csv", "a")
        for LiIds in range(1, 25):
            LiId = "newslist-"+str(LiIds)

            try:
                sp = soup.find('li', {"id": LiId})
                title = sp.find('h2').get_text().replace(
                    "\n", "").replace(",", "--").strip()
                link = sp.find('a').get('href')
                date = sp.find('span').get_text()
                date = dts.moneyctl(date)

            except:
                error = error+1
                continue

            outs = str(title)+","+str(link)+","+str(date)+"\n"

            # print(outs)
            try:
                output_file.write(outs)
            except:
                error = error+1
                print("Error encoding to file: ",page)
        output_file.close()
    except:
        print("Error: ",url)


def downloadMtlUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"class": "artTitle"}).get_text()
    data = ""

    date = soup.find('div', {'class': 'arttidate'}).get_text().replace(
        "Last Updated : ", "").replace('| Source: Moneycontrol.com', "").strip()

    sp = soup.find('div', {"id": "article-main"})
    for p in sp.findAll('p'):
        o = p.get_text()
        if(not o.startswith("Disclaimer")):
            data = data + o.replace("\n", "").replace("\"", "")

    print(dts.moneyctl2(date))
    return(title, data)


downloadMtlUrl('https://www.moneycontrol.com/news/business/stocks/fibonacci-retracement-suggests-nifty-may-touch-12250-before-bears-make-an-entry-4681951.html')
# if __name__ == '__main__':
#     for pages in range(221, 300):
#         page = "page-"+str(pages)
#         a = downloadMtlAll(
#             "https://www.moneycontrol.com/news/business/"+page, "all-1.csv")
#     print("Total errors:", error)
