

import argparse
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
import json
from math import floor
import requests
from requests.utils import cookiejar_from_dict

from notion_api import Properties
from notion_api import DatabaseParent
from notion_api import Children
from notion_api import Page
from util import get_title
import unsplash
import notion_api
from config import BOOK_DATABASE_ID
WEREAD_BASE_URL = "https://weread.qq.com/"
WEREAD_HISTORY_URL = (
    "https://i.weread.qq.com/readdetail?baseTimestamp=0&count=32&type=1"
)

def parse_cookie_string(cookie_string):
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies_dict = {}
    cookiejar = None
    for key, morsel in cookie.items():
        cookies_dict[key] = morsel.value
        cookiejar = cookiejar_from_dict(
            cookies_dict, cookiejar=None, overwrite=True
        )
    return cookiejar


def get_reading(minutes):
    filter = {"property": "状态", "select": {"equals": "在读"}}
    response = notion_api.query_database(BOOK_DATABASE_ID, filter)
    for result in response["results"]:
        name = get_title(result,"标题")
        id = result["id"]
        url = result["properties"]["条目链接"]["url"]
        insert(name,id,minutes,url)


def insert(title, id,minutes,url):
    properties = (
        Properties()
        .title(title)
        .relation("Book", id)
        .url("URL",url)
        .number("时长", minutes)
        .date(start=datetime.now())
    )
    properties = notion_api.get_relation(properties)
    page = (
        Page()
        .parent(DatabaseParent("cca71ece15ac48a68c34e5f86a2e6b38"))
        .children(Children())
        .properties(properties)
        .cover(unsplash.random())
        .icon("📚")
    )
    notion_api.create_page(page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cookie")
    options = parser.parse_args()
    session = requests.Session()
    session.cookies = parse_cookie_string(options.cookie)
    r = session.get(WEREAD_HISTORY_URL)
    with open('r.json','w') as f:
        f.write(json.dumps(r.json()))
    if not r.ok:
        # need to refresh cookie WTF the design!!
        if r.json()["errcode"] == -2012:
            session.get(WEREAD_BASE_URL)
            r = session.get(WEREAD_HISTORY_URL)
    if r.ok:
        day = datetime.now().day
        seconds = r.json()['datas'][0]['timeMeta']['readTimeList'][day-1]
        minutes = floor(seconds/60)
        get_reading(minutes)
