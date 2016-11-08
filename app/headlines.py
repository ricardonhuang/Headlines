#coding=utf-8
'''
Created on 2016��11��2��

@author: huangning
'''
from flask import Flask ,render_template,request,make_response
import feedparser
import json,urllib,urllib2,datetime


app = Flask(__name__)
publications = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
'xinhuafangchan': 'http://www.xinhuanet.com/house/news_house.xml',
'fox': 'http://feeds.foxnews.com/foxnews/latest',
'tecent_news': 'http://news.qq.com/newsgn/rss_newsgn.xml'}

DEFAULTS={'publication':'bbc','city':'London,UK'}

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

@app.route("/")
def home():
    # get customized headlines, based on user input or default
    # get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # get customised weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather (city)
    
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             publications=publications))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    return response

def get_news(query):
    publication = query.lower()
    feed = feedparser.parse(publications[publication])
   
    #print len(feed)
    #print feed
    #first_article = feed['entries'][0]
    return feed['entries']


#api参数：units=metric 返回标准摄氏温度，&#8451 在HTML中显示摄氏温度符号，&#8457 华氏温度符号
def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=30c92e4388487068934889f679adb092'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   'country': parsed['sys']['country']
                   }
    return weather

'''openweathermap_api:  30c92e4388487068934889f679adb092'''


if __name__ == '__main__':
    app.run(port=5000, debug=True)
