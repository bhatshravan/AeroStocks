from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
from datetime import timedelta, date
from bs4 import BeautifulSoup

import csv
import pandas as pd


def LoughranMcDonald(data):

    # stock market lexicon
    stock_lex = pd.read_csv('../data/classifier/stock_lex.csv')
    stock_lex['sentiment'] = (
        stock_lex['Aff_Score'] + stock_lex['Neg_Score'])/2
    stock_lex = dict(zip(stock_lex.Item, stock_lex.sentiment))
    stock_lex = {k: v for k, v in stock_lex.items() if len(k.split(' ')) == 1}
    stock_lex_scaled = {}
    for k, v in stock_lex.items():
        if v > 0:
            stock_lex_scaled[k] = v / max(stock_lex.values()) * 4
        else:
            stock_lex_scaled[k] = v / min(stock_lex.values()) * -4

    # # Loughran and McDonald
    # positive = []
    # with open('../data/classifier/lm_positive.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         positive.append(row[0].strip())

    # negative = []
    # with open('../data/classifier/lm_negative.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         entry = row[0].strip().split(" ")
    #         if len(entry) > 1:
    #             negative.extend(entry)
    #         else:
    #             negative.append(entry[0])

    final_lex = {}
    # final_lex.update({word:2.0 for word in positive})
    # final_lex.update({word:-2.0 for word in negative})
    final_lex.update(stock_lex_scaled)
    final_lex.update(sia.lexicon)
    sia.lexicon = final_lex


def vaderAtOnce(data):
    if(data == "none"):
        return("none", 0.0, 0.0, 0.0)

    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(data)

    pos = vs['pos']
    neg = vs['neg']
    neu = vs['neu']

    # print(data, "-\n", pos, neg, neu)
    print("Input - {}\nPositivity - {}\nNegativity - {}\nNeutrality - {}".format(data, pos, neg, neu))
    polarity = round(pos-neg, 3)

    if(pos > neg):
        return("Positive", pos, neg, neu)
    else:
        return("Negative", pos, neg, neu)


def vaderParagraph(heading, data):

    analyzer = SentimentIntensityAnalyzer()

    if(data == "none"):
        return("none", 0.0, 0.0, 0.0)

    sentence_list = tokenize.sent_tokenize(data)
    paragraphSentiments = 0.0
    for sentence in sentence_list:
        vs = analyzer.polarity_scores(sentence)
        paragraphSentiments += vs["compound"]

    pos_words = ["rally"]

    neg_words = ["plunge up to", "share price falls", "shares fall","shares dip","stock plunges","profit plunges","drops over","plummets"
                 "52-week low", "nosedives", "share price tanks", "-yr low", "slides", "dips"]

    spec_words = ["Buzzing stocks", "ideas from experts"]

    averageSentiment = round(paragraphSentiments / len(sentence_list), 4)

    heading = heading.lower()

    for words in spec_words:
        if words in heading:
            return(0)

    for words in neg_words:
        if words in heading:
            if(averageSentiment > 0):
                averageSentiment = -1*averageSentiment
            return(averageSentiment)
    
    for words in pos_words:
        if words in heading:
            if(averageSentiment < 0):
                averageSentiment = -1*averageSentiment
            return(averageSentiment)

    return ((averageSentiment))


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
