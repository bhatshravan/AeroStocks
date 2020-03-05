from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


import requests
from datetime import timedelta, date
from bs4 import BeautifulSoup


def vaderAtOnce(data):
    if(data == "none"):
        return("none", 0.0, 0.0, 0.0)

    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(data)

    pos = vs['pos']
    neg = vs['neg']
    neu = vs['neu']

    print(data, "\n -", pos, neg, neu)
    polarity = round(pos-neg, 3)

    if(pos > neg):
        return("Positive", pos, neg, neu)
    else:
        return("Negative", pos, neg, neu)


def vaderWords(data):

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

    pos_word_list = []
    neu_word_list = []
    neg_word_list = []
    overall = 0
    l = data
    l = l.lower()

    for word in l.split():
        overall = overall + sid.polarity_scores(word)['compound']
        if (sid.polarity_scores(word)['compound']) >= 0.02:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.02:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)

    overall = round(overall, 3)

    if(overall < -0.1):
        return("Negative", overall)
    elif(overall > 0.1):
        return("Positive", overall)
    else:
        return("Neutral", overall)
