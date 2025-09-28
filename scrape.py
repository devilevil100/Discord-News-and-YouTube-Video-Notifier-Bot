from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
import json

def stockmarket():
    r = Request('https://de.investing.com/news/stock-market-news', headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(r).read()
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all(class_ = "js-article-item")

    result = []
    base = {}

    for bl in table:
        news = bl.find(class_ ="title").text
        link = bl.find(class_ ="title").get('href')
        if not link.startswith('/news/'):
            continue
        result.append({'title': news, 'link': "https://de.investing.com/"+link})
    return result

def cryptocurrency():
    r = Request('https://de.investing.com/news/cryptocurrency-news', headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(r).read()
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all(class_ = "js-article-item")

    result = []
    base = {}

    for bl in table:
        news = bl.find(class_ ="title").text
        link = bl.find(class_ ="title").get('href')
        if not link.startswith('/news/'):
            continue
        result.append({'title': news, 'link': "https://de.investing.com/"+link})
    return result

def economy():
    r = Request('https://de.investing.com/news/economy', headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(r).read()
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all(class_ = "js-article-item")

    result = []
    base = {}

    for bl in table:
        news = bl.find(class_ ="title").text
        link = bl.find(class_ ="title").get('href')
        if not link.startswith('/news/'):
            continue
        result.append({'title': news, 'link': "https://de.investing.com/"+link})
    return result
