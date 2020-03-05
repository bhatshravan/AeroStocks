# Imports

import math
from datetime import datetime, timedelta
import requests
from datetime import timedelta, date
from bs4 import BeautifulSoup
import re

# Variables
url = "https://www.deccanherald.com/business/business-news/private-sector-salaries-show-slowest-growth-in-10-years-755915.html"
initalUrl = "https://www.deccanherald.com"

global output_file
output_file = open("../test", "a")


def extractUrl(url):
    return(re.findall("\(|\)|\d{6}|\(|\)|\d{5}", url))


def downloadUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('h1', {"id": "page-title"}).get_text()

    contents = soup.find_all('div', {"class": "content"})
    data = ""
    for content in contents:
        data = data + content.get_text().replace("\n", "").replace("\"", "")

    print(title)
    print(data)


downloadUrl(url)
