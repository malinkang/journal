

import argparse
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
import requests
from requests.utils import cookiejar_from_dict

from notion_api import Properties
from notion_api import DatabaseParent
from notion_api import Children
from notion_api import Page
import unsplash
import notion_api


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
    response = notion_api.query_database("c7efdba75f4146ad84a3f5b773998859", filter)
    if len(response.get("results")) > 0:
        name = notion_api.get_title(response, "标题")
        id = response.get("results")[0].get("id")
        insert(name,id,minutes)


def insert(title, id,minutes):
    properties = (
        Properties()
        .title(title)
        .relation("Book", id)
        .number("时长", minutes)
        .date(start=datetime.now-timedelta(days=1))
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
    r = session.get("https://i.weread.qq.com/readdetail?baseTimestamp=0&count=32&type=1")
    day = (datetime.now()-timedelta(days=1)).day
    seconds = r.json()['datas'][0]['timeMeta']['readTimeList'][day-1]
    minutes = round(seconds/60)
    get_reading(minutes)
