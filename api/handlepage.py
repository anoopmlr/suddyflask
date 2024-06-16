# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:50:26 2023

@author: mylar
"""
#from flask import Blueprint
import datetime;
from pytz import timezone
from pymongo import MongoClient
import pymongo
import requests
from bs4 import BeautifulSoup

#handlepage = Blueprint("handlepage", __name__)

def add_itv(itvurl, mainclassname):
    r = requests.get(itvurl)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_=mainclassname)
    contentList = s.find_all('a')
    return contentList

# Function to crawl news page and translate to json.
def add_news_itv(contentList, category):
    dbname = get_database()
	# Create a new collection
    collection_name = dbname["news_items"]
    #collection_name.insert_one(item_1)
    format = "%Y-%m-%dT%H:%M:%S%z"
    news_now = datetime.datetime.now(timezone('Asia/Kolkata'))
    for i in contentList:
      newsDate = news_now.strftime(format)
      # Making a GET request
      techurl = i.attrs.get('href', 'Not found')
      print(techurl)
      req = requests.get(techurl)
      soup = BeautifulSoup(req.content, 'html.parser')
      datePub = soup.findAll('meta', {'property':'article:published_time'})
      publishedDate = datePub[0]['content']
      print("datePub: " + publishedDate)
      s = soup.find('div', class_='row two_column')
      header1Data = s.find_all('h1')
      header2Data = s.find_all('h2')
      title = header1Data[0].text
      description = header2Data[0].text
      print("title: " +title)
      print("description: " +description)
      sContent = soup.find('div', class_='content')
      lines = sContent.find_all('p')
      figureData = sContent.find('figure', class_='artbigimg row')
      imgD2 = figureData.find_all('img')
      for imgOrigin2 in imgD2:
        print("imgOrigin:  " + imgOrigin2['data-original'])
        imageurl = imgOrigin2['data-original']
      print(imageurl)
      authurData = soup.find('span', class_='author-name')
      authorName = authurData.find_all('a')
      author = authorName[0].text
      print("auther name: "+ author)
      contentData = lines[0].text
      print("content: " + contentData)
      urlsize = len(techurl)
      if urlsize >= 20:
          techurl_id = techurl[urlsize-17:urlsize]
      else:
          techurl_id = techurl
      
      if publishedDate is None:
          publishedDate = newsDate
          
      newsitem = {
          "_id": techurl_id,
          "category": category,
          "newsDate": newsDate,
          "author": author,
          "title": title,
          "description": description,
          "url": techurl,
          "urlToImage": imageurl,
          "publishedAt": publishedDate,
          "content": contentData
      }
      print('techurl_id' + techurl_id)
      #collection_name.insert_one(newsitem)
      try:
          collection_name.insert_one(newsitem)
      except pymongo.errors.DuplicateKeyError:
          print('ignore duplicate error')
      print('\n')
         
    return "success"

def insert_news_feeds(payload):
    sourceId = payload['sourceId']
    source = payload['source']
    mainclassname = payload['mainclassname']
    url = payload['url']
    category = payload['category']
    description = payload['description']
    feedDate = current_time()
    dbname = get_database()
    news_feeds = dbname["news_feeds"]
    newsfeed = {
        "_id": source + category,
        "sourceId": sourceId,
        "feedDate": feedDate,
        "source": source,
        "mainclassname": mainclassname,
        "description": description,
        "url": url,
        "category": category
    }
    result_message = "insert feed success"
    try:
        news_feeds.insert_one(newsfeed)
    except pymongo.errors.DuplicateKeyError:
        result_message = "ignore duplicate news feed error"
    return result_message


def update_news_feeds(payload):
    sourceId = payload['sourceId']
    source = payload['source']
    mainclassname = payload['mainclassname']
    url = payload['url']
    category = payload['category']
    description = payload['description']
    feedDate = current_time()
    dbname = get_database()
    news_feeds = dbname["news_feeds"]
    newsfeed = {
        "_id": source + category,
        "sourceId": sourceId,
        "feedDate": feedDate,
        "source": source,
        "mainclassname": mainclassname,
        "description": description,
        "url": url,
        "category": category
    }
    result_message = "update feed success"
    try:
        news_feeds.update_one(newsfeed)
    except pymongo.errors.DuplicateKeyError:
        result_message = "update news feed error"
    return result_message

def current_time():
    format = "%Y-%m-%dT%H:%M:%S%z"
    news_now = datetime.datetime.now(timezone('Asia/Kolkata'))
    newsDate = news_now.strftime(format)
    return newsDate

# Function to crawl news page and translate to json.
def retrieve_news_feeds():
    dbname = get_database()
	# Create a new collection
    news_feeds = dbname["news_feeds"]
    return news_feeds

# Function to crawl news page and translate to json.
def retrieve_news(categorySelected, pagesize):
    dbname = get_database()
	# Create a new collection
    collection_name = dbname["news_items"]
    # Organize documents in order from latest news to oldest.
    news_data_order = {"$sort": {"newsDate": -1}}
    #Select news based on category.
    select_category = {"$match": {"category": categorySelected}}
    news_data_limit = {"$limit": pagesize}

    
    # Create an aggegation pipeline containing the four stages created above
    pipeline = [
        news_data_order,
        select_category,
        news_data_limit
    ]
    
    # Perform an aggregation on 'pipeline'.
    results = collection_name.aggregate(pipeline)
    return results
    #return collection_name.find(limit=5)


def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   #CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
   #CONNECTION_STRING = "mongodb+srv://mylar123:wSs1QMAbw0gjOG2C@cluster0.yhcddkj.mongodb.net/newsDatabase"
   CONNECTION_STRING = "mongodb://admin:admin@DESKTOP-QJK86L8:27017/newsDatabase?authSource=admin&retryWrites=true&w=majoritynew"
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our en
   return client['news_content_list']