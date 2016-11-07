#coding=utf-8
'''
Created on 2016��11��2��

@author: huangning
'''
from flask import Flask ,render_template,request
import feedparser


app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
'xinhuafangchan': 'http://www.xinhuanet.com/house/news_house.xml',
'fox': 'http://feeds.foxnews.com/foxnews/latest',
'tecent_news': 'http://news.qq.com/newsgn/rss_newsgn.xml'}

@app.route("/",methods=['GET','POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
        
    feed = feedparser.parse(RSS_FEEDS[publication])
    #print len(feed)
    #print feed
    #first_article = feed['entries'][0]
    for article in feed['entries']:
        print article.summary
    return render_template("home.html",articles=feed['entries'])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
