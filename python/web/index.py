import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, send_from_directory
import json
import urllib.request
import os
import random
import tensorflow as tf

# template_dir = os.path.abspath('../../website/templates/')
app = Flask(__name__)


@app.route('/topnews')
def topnews():
    url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=45bb840c98934815a19ec6784fc50a19&category=business"
    response = requests.get(url)
    data = response.json()
    return str(data["articles"])


@app.route('/')
def root():
    # return render_template('index.html') 
    return "Hello world"

@app.route('/getstocks')
def getstocks():
    api_key = ["D4V3YEYJGNXZ27PL", "BEZAPQ60MX6M0MTV", "C73M71O6LA04D9KI",
           "4D5AD7GG5BUJ0R9Y", "5LIB86FZXJJ5YQD3", "LK8JHRNLLTU90Q9C"]

    rand_key = api_key[random.randrange(0, len(api_key))]
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE&apikey=" + \
        rand_key+"&datatype=json&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    return str(data)


@app.route('/getnse')
def getstocks2():
    url = "https://www.moneycontrol.com/techmvc/mc_apis/market_action/?classic=false&section=sectoral_indices&limit=2"
    response = requests.get(url)
    data = response.json()
    return str(data["sectoral_indices"]["data"][0]["last_price"])


@app.route('/getprediction')
def getmodel():
    vader = request.args.get('vader')
    secscore = request.args.get('secscore')
    assoc = request.args.get('assoc')
    model = tf.keras.models.load_model('../classifier/models/model2.h5')
    predictions = model.predict([[0.3,0.9,2]])
    # return(str(predictions[0][0]))
    return(str(language))

if __name__ == '__main__':
	app.run(debug=True, port=8080)
    # getmodel()