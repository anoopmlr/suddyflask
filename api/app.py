from flask import Flask, Response, jsonify, request

from .errors import errors

#import requests
import api.handlepage
#from api.handlepage import handlepage
#from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(errors)



@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@app.route('/addnewsitv')
def addnews():
    #r = requests.get('https://www.indiatvnews.com/health')
    #mainclassname = 'row lhsBox sport_tnews mb20'
    techurl = "https://www.indiatvnews.com/technology"
    healthurl = "https://www.indiatvnews.com/health"
    entertainmenturl = "https://www.indiatvnews.com/entertainment"
    #sportsurl = "https://www.indiatvnews.com/sports"
    #businessurl = "https://zeenews.india.com/business"
    
    
    contentList = api.handlepage.add_itv(techurl, 'big-news-list')
    api.handlepage.add_news_itv(contentList, 'technology')
    
    contentList = api.handlepage.add_itv(healthurl, 'row lhsBox sport_tnews mb20')
    api.handlepage.add_news_itv(contentList, 'health')
    
    contentList = api.handlepage.add_itv(entertainmenturl, 'row lhsBox sport_tnews')
    api.handlepage.add_news_itv(contentList, 'entertainment')
    
    #contentList = api.handlepage.add_itv(sportsurl, 'row lhsBox sport_tnews mb20')
    #api.handlepage.add_news_itv(contentList, 'sports')

    #if category == "business":
     #   r = requests.get(businessurl)
      #  mainclassname = 'section-tumbnail-container'

    return jsonify({"success": "added news data for itv"})


@app.route('/addnews')
def addnewsFromNewsFeeds():
    news_feeds = api.handlepage.retrieve_news_feeds()
    for feed in news_feeds:
        contentList = api.handlepage.add_itv(feed['url'], feed['mainclassname'])
        api.handlepage.add_news_itv(contentList, feed['category'])
    return Response("OK", status=201)

@app.route('/addnewsfeeds', methods=["POST"])
def addnewsattribute():
    payload = request.get_json()
    message = api.handlepage.insert_news_feeds(payload)    
    return jsonify({"status": message})

@app.route('/updatenewsfeeds', methods=["PUT"])
def updatenewsattribute():
    payload = request.get_json()
    message = api.handlepage.insert_news_feeds(payload)    
    return jsonify({"status": message})

@app.route('/newsdata')
def retrievenewsdata():
    
    args = request.args
    #name = args.get('name')
    #location = args.get('location')
    #print(type(args))
    #print("name: " + name + "localtion : "+ location)
    category = args.get('category')
    if category is None:
        category = "general"
    print("category: " + category)
    pagesize = 2
    pagesize = args.get('pagesize')
    if pagesize is None or int(pagesize) < 1:
        pagesize = 5
    
    # Define Variable
    status = "ok"
    newsdata = list(api.handlepage.retrieve_news(category, int(pagesize)))
    constJSON = {"status":status, "totalResults":len(newsdata), "articles":newsdata}
    
    #return jsonify(constJSON[0])
    return jsonify(constJSON)

@app.route("/health")
def health():
    return Response("OK", status=200)
