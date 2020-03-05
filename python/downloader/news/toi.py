import argparse
import logging
import requests
from bs4 import BeautifulSoup
from slugify import slugify

FORMAT = '%(asctime)-15s [%(levelname)s] : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.CRITICAL)

FLAG = False


def scrapper(args):
    logging.info("catching url %s", args)
    response = requests.get(url=args)
    logging.info("responce code %s", response.status_code)
    try:
        soup = BeautifulSoup(response.text, "html5lib")
        time_stamp = soup.find("span", {"class": "time_cptn"})
        logging.info("article updated on : %s", time_stamp.get_text())
        logging.info("page title found: %s", soup.title.get_text())
        arttitle = soup.arttitle.get_text()
        logging.info("article title found: %s", arttitle)
        summary = soup.find("div", {"class": "artsyn"})
        arttextxml = soup.arttextxml.get_text()
        print("\nArticle Title: \n\n", arttitle)
        print("\nArticle Body: \n\n", arttextxml)
        print("\nArticle Summary: \n\n", summary.get_text())
        if FLAG:
            file = open(slugify(arttitle) + ".txt", 'a')
            file.write("Title: " + arttitle + "\n\n")
            file.write("Body: " + arttextxml + "\n\n")
            file.write("Summary: " + summary.get_text() + "\n\n")
            file.close()
    except AttributeError:
        logging.error("TOI article not found")
        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="[REQUIRED] TOI url")
    parser.add_argument(
        "-o", "--output", help="[OPTIONAL] this will save output into text file", action="store_true")
    args = parser.parse_args()
    if args.output:
        FLAG = True
    if args.url:
        scrapper(args.url)
    else:
        logging.warning("Something went wrong")
