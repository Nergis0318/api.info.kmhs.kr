import datetime as dt
import re

import feedparser
import requests
from bs4 import BeautifulSoup

rss_url = "https://kmh-h.goeay.kr/kmh-h/na/ntt/selectRssFeed.do?mi=5589&bbsId=2405"
date_now = dt.datetime.now()
date_kor = "1월7일"
rss_data = feedparser.parse(rss_url)["entries"]
count = 0


# noinspection PyTypeChecker
for i in rss_data:
    if re.search(r"^\[메뉴사진].*$", i["title"]) and count == 0:
        url = i["link"].replace("/kmh-h/na/ntt/kmh-h/na/ntt/", "/kmh-h/na/ntt/")
        print(url)
        response = requests.get(url)
        html = BeautifulSoup(response.text, "html.parser")
        try:
            # noinspection PyUnresolvedReferences
            img_url = "https://kmh-h.goeay.kr" + html.find("img", alt=date_kor)["src"]
            count += 1
        except TypeError:
            continue
        print(img_url)
        print(dt.datetime.today())
