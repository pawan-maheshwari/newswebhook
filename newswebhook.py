import json
import os
import requests
import sys
import eikon as tr
import numpy as np
import pandas as pd
import cufflinks as cf
import configparser as cp
import nltk, bs4

from flask import Flask
from flask import request
from flask import make_response



# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    if req.get("result").get("action") != "fetchNews":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    ticker = parameters.get("ticker")
    if ticker is None:
        return None
    tr.set_app_key('229dfa317f614c3c9cdfa2908c1ff66af4fdf1c6')
    r = tr.get_news_headlines('ticker',date_from='2020-03-09',date_to='2020-03-10',count=5)
    r.head()
    news = r("text")
    print(news)
   
    result = "The news on"+ticker+"are"+news
    return {
        "text": result,
            }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















