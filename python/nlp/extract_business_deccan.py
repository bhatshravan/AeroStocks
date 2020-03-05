import pandas as pd
import glob
import nltk

import spacy
from textblob import TextBlob

raaw = ["The new Galaxy A90 5G series launched Photo Credit: SamsungWorlds leading smartphone-maker Samsung on Tuesday unveiled the new Galaxy A90 5G in the home country South Korea.As the name suggests, the new Galaxy A90 series supports 5G network, a first for non-flagship S or Note series Samsung phone. It houses Qualcomm Snapdragon 855 octa-core processor with X50 modem. With such hardware, the device owner can enjoy peak internet speed up to 5Gbps to 10 Gbps. This means users can download 4K resolution multimedia contents with sizes as big as 8GB or more in just a few seconds. Also, consumers can also watch HDR 10+ video content on media streaming apps without any buffering.The Galaxy A90 5G is also the first Galaxy A series phone to support Samsung Dex. This feature allows the users to connect their Galaxy A90 5G to their PC screen or TV and work with One UI same as using a phone, but on a large monitor. Also, they can use the Microsoft Your Phone app to mirror phone display onto their desktop to check notifications, send and receive messages, and browse through recent photos.Another notable aspect of the Galaxy A90 5G is the photography hardware. It boasts triple camera module, one a 48MP, 8MP ultra-wide-angle lens and a 5MP sensor on the back with LED flash and a 32MP selfie shooter on the front."]


# nlp = spacy.load('en_core_web_sm')
# doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)


def extractBuisnessNews():
    files = (glob.glob("../data/news/deccan/*.csv"))
    for file in files:
        data = pd.read_csv(file)
        headline = data[data.category.str.contains(
            'Business')][['headline', 'date', 'link']]
        print(headline)
        headline.to_csv('../data/news/deccan/sample1.csv',
                        header=True, index=False)


def vaderAnalysis():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # data = pd.read_csv("file2.csv")
    # data = data['headline'].values.tolist()
    # print(data)
    data = "The shares of Tata's watch and jewellery arm Titan rallied by 1.65 % on Monday despite bloodbath in the global equity markets, as the company announced encouraging performance in the jewellery sales segment during the December quarter. The share of t..."
    # Vader analysis

    analyzer = SentimentIntensityAnalyzer()
    pos = 0
    neg = 0

    # for raaw2 in raaw.split("."):
    raaw2 = "Mahindra and Mahindra's sales fall 25% in August"
    vs = analyzer.polarity_scores(raaw2)
    pos = pos+vs['pos']
    neg = neg+vs['neg']
    print("{:-<65} {}".format(raaw2, str(vs)))
    print(pos, neg)

    # analyzer = SentimentIntensityAnalyzer()
    # for sentence in data:
    #     vs = analyzer.polarity_scores(sentence)
    #     print("{:-<65} {}".format(sentence, str(vs)))

    data = pd.read_csv("./..//data/news/deccan/sample1.csv")
    data = data['headline'].values.tolist()


def nltkClassifier():
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    pos_word_list = []

    neu_word_list = []
    neg_word_list = []

    overall = 0
    # raaw = ["European shares dip, pound at its lowest since Jan 2017"]
    for l in raaw:
        blob = TextBlob(l)
        # for sentence in blob.sentences:
        #     print(sentence.sentiment.polarity, sentence)
        l = l.lower()
        for word in l.split():
            # print(sid.polarity_scores(word)['compound'], word)
            overall = overall + sid.polarity_scores(word)['compound']
            if (sid.polarity_scores(word)['compound']) >= 0.02:
                pos_word_list.append(word)
            elif (sid.polarity_scores(word)['compound']) <= -0.02:
                neg_word_list.append(word)
            else:
                neu_word_list.append(word)
    if(overall < -0.08):
        print("Negative news")
    elif(overall > 0.08):
        print("Positive news")
    else:
        print("Neutral news")
    # print('\n\nPositive :', pos_word_list)
    # print('\n\nNeutral :', neu_word_list)
    # print('Negative :', neg_word_list)
    print(overall)


def weird(sentence):
    # print(sentence)
    import string
    from spacy.lang.en.stop_words import STOP_WORDS
    from spacy.lang.en import English

    # Create our list of punctuation marks
    punctuations = string.punctuation

    # Create our list of stopwords
    nlp = spacy.load('en_core_web_sm')
    stop_words = spacy.lang.en.stop_words.STOP_WORDS

    # Load English tokenizer, tagger, parser, NER and word vectors
    parser = English()

    # mytokens = nlp(sentence)

    # Creating our tokenizer function
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)

    # for word in mytokens:
    #     print(word.lemma_)
    # if word.lemma_ != "-PRON-"

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [word.lemma_.lower().strip() for word in mytokens]

    # Removing stop words
    mytokens = [
        word for word in mytokens if word not in stop_words and word not in punctuations]

    # return preprocessed list of tokens
    return mytokens


def spacyClassifier():
    from spacy.lang.en.stop_words import STOP_WORDS
    from spacy.lang.en import English
    import string

    nlp = English()

    # Implementation of stop words:

    for text in data:
        # doc = nlp(text)

        # # filtering stop words
        # filtered_sent = []
        # for word in doc:
        #     if word.is_stop == False:
        #         filtered_sent.append(str(word))

        # fil = " ".join(filtered_sent)
        fil = " ".join(weird(text))
        print(fil, " ", text)


def spacies(sentence):
    import spacy
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(sentence)

    for token in doc:
        print(token.text, token.lemma_, token.pos_)

    for word in data:
        doc = nlp(word)
        print([(token.text, token.label_) for token in doc.ents])


def bagofText():
    from nltk.classify import NaiveBayesClassifier

    pos_words = []
    neg_words = []

    for pos_word in open('../data/classifier/positive-words.txt', 'r').readlines()[1:]:
        pos_words.append(({pos_word.rstrip(): True}, 'positive'))

    for neg_word in open('../data/classifier/negative-words.txt', 'r').readlines()[1:]:
        neg_words.append(({neg_word.rstrip(): True}, 'negative'))

    classifier = NaiveBayesClassifier.train(pos_words + neg_words)

    test_data = []
    data = "The equities in Indian markets were the worst hit across the globe on Monday’s trade, as the escalating geopolitical tensions US and Iran forced global investors to move their allocations towards safer assets.The 30-share Sensex of BSE tanked by 1.90% (787.98 points) during the day’s trade to close at 40,676.63 points. On Friday, the index, which was witnessing heavy buying in the past few months cracked by 162 points, as the news of the US military attack killing Iran’s top General Qasim Soleimani poured in.On Monday, the market breadth was heavily negative, with 593 advances compared with 1,935 declines.During the day’s trade Indian investors were poorer by Rs 3.01 lakh crore – losing 1.9% of their wealth, as all the indices on the BSE, including the consumer durables traded in the red. Among the sectoral indices, finance, energy, realty and oil & gas were the worst hit.The broader exchange Nifty50 also closed with a loss of 1.91% (233.6 points) at 11,993.05. The tension also affected the Indian rupee which was the worst-performing currency among the Asian emerging markets on Monday.Other than India, Japan’s Nikkei 225 Index cracked 1.91%, Germany’s DAX Performance Index cracked 1.76%, Turkey’s BIST 100 1.66%.“Long overdue correction was looking for a trigger which has happened. In the longer-term pension allocations may ensure a softer than expected landing,” said Anubhav Shrivastava, Partner, Infinity Alternatives.Experts suggest that the Japanese market is the first stock market to open, hence it suffered the maximum loss such a huge loss. The loss in the Indian equities was furthered by the fact that both Sensex and Nifty had seen a massive rally since the reduction of Corporate tax rates in September last year and correction was waiting for a trigger, according to analysts.On the currency front, Rupee was the worst performer in Asia’s emerging markets basket losing 25 paise (0.35%) on Monday on top of 42 paise loss on Friday. The rupee was trading at 72.04 against the US dollar.  Other than a rupee, Korean Wong crashed 0.43%, Peruvian Sol cracked 0.48% and Brazilian Lira cracked up 0.84%.However, as the global investors withdrew monies from the global stock markets, the prices of gold, seen as a safer asset, surged by $1,576.37 per ounce, jumping by 3.4%."

    text = data
    # for text in data:
    # text_to_classify = to_dictionary(text.split())
    ttsx = weird(text)
    text_to_classify = to_dictionary(ttsx)
    # print(text_to_classify)
    result = classifier.classify(text_to_classify)
    print(text, "-", result)
    # text_to_classify = to_dictionary(raaw[0])
    # result = classifier.classify(text_to_classify)
    # print(text_to_classify, "-", result)


def to_dictionary(words):
    return dict([(word, True) for word in words])


if __name__ == "__main__":
    # nlp = spacy.load('en_core_web_sm')
    #     print(spacies(word), word)
    # if token.pos_ == "ADV":

    # for word in data:
    #     spacies(word)

    # print(spacies(data[0]))
    # bagofText()

    # nltkClassifier()

    bagofText()
    # vaderAnalysis()
    # nlp = spacy.load('en_core_web_sm')
    # spacies("word")

    # nltkClassifier()
