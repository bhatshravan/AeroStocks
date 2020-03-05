# https: // economictimes.indiatimes.com/lazyloadlistnew.cms?msid = 2146843 & curpg = 100 & img = 0
import requests
from bs4 import BeautifulSoup

# # specify the url
page = 'https://economictimes.indiatimes.com/lazyloadlistnew.cms?msid=2146843&curpg=100&img=0'

# get_page = ur.urlopen(page)

# # parse the html page and store in a variable
# parsed_content = BeautifulSoup(get_page, 'html.parser')

# content = parsed_content.find('div', attrs={'class': 'eachStory'})

# # get only data
# content_data = content.text

# # print data
# print(content_data)


response = requests.get(page)
soup = BeautifulSoup(response.content, "html.parser")
print(soup)
