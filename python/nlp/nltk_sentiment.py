def nltkClassifier(data, types):

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    pos_word_list = []

    neu_word_list = []
    neg_word_list = []

    overall = 0
    l = data
    blob = TextBlob(l)
    l = l.lower()
    for word in l.split():
        #         print(sid.polarity_scores(word)['compound'], word)
        overall = overall + sid.polarity_scores(word)['compound']
        if (sid.polarity_scores(word)['compound']) >= 0.02:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.02:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)
    overall = round(overall, 3)
    if(overall < -0.1):
        print("NLTK  -", types, ", Negative news = ", overall)
    elif(overall > 0.1):
        print("NLTK  -", types, ", Positive news = ", overall)
    else:
        print("NLTK  -", types, ", Neutral  news = ", overall)
