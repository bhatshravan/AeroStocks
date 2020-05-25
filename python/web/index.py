import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, send_from_directory
import json
import urllib.request
import os
import random
import test as getNewsApi
import tensorflow as tf

# template_dir = os.path.abspath('../../website/templates/')
app = Flask(__name__)


@app.route('/topnews')
def topnews():
    data = getNewsApi.main()
    return data


@app.route('/mtlnews')
def mtlnews():
    data = getNewsApi.downloadMtlNews()
    return data



@app.route('/')
def root():
    # return render_template('index.html') 
    return "Stock Market"

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
    vader = float(request.args.get('vader'))
    secscore = request.args.get('secscore')
    assoc = request.args.get('assoc')
    model = tf.keras.models.load_model('../classifier/models/model2.h5')
    predictions = model.predict([[float(vader),float(secscore),float(assoc)]])
    # return(str(vader))
    return("Input:"+str(vader)+"\nScore:"+str(predictions[0][0]))

if __name__ == '__main__':
	app.run(debug=True, port=8080)