import datetime as dt
import json
import os
import re

import feedparser
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pycomcigan import TimeTable
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/timetable")
async def main(grade: int, classnum: int):
    td = {"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": ""}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = TimeTable("근명고등학교", week_num=0)

    for i in range(0, 5):
        td[days[i]] = str(timetable.timetable[grade][classnum][i + 1])

    return td


@app.get("/mealimg")
async def mealimg():
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    file_path = "mealimg.json"
    data = (
        json.load(open(file_path, "r", encoding="utf-8"))
        if os.path.exists(file_path)
        else {}
    )
    if today_str in data:
        return PlainTextResponse(data[today_str])

    rss_url = "https://kmh-h.goeay.kr/kmh-h/na/ntt/selectRssFeed.do?mi=5589&bbsId=2405"
    date_now = dt.datetime.now()
    date_kor = f"{date_now.month}월{date_now.day}일"
    rss_data = feedparser.parse(rss_url)["entries"]

    for item in rss_data:
        if re.search(r"^\[메뉴사진].*$", item["title"]):
            url = item["link"].replace("/kmh-h/na/ntt/kmh-h/na/ntt/", "/kmh-h/na/ntt/")
            response = requests.get(url)
            html = BeautifulSoup(response.text, "html.parser")
            try:
                img_url = (
                    "https://kmh-h.goeay.kr" + html.find("img", alt=date_kor)["src"]
                )
                data[today_str] = img_url
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
                return PlainTextResponse(img_url)
            except TypeError:
                return JSONResponse(
                    status_code=404,
                    content={"message": "이미지 URL을 찾을 수 없습니다."},
                )
    return None
