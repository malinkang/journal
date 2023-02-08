

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
from util import get_rich_text
from config import BOOK_DATABASE_ID

WEREAD_BASE_URL = "https://weread.qq.com/"
WEREAD_HISTORY_URL = (
    "https://i.weread.qq.com/book/readinfo"
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


def get_reading():
    filter = {"property": "状态", "select": {"equals": "在读"}}
    response = notion_api.query_database(BOOK_DATABASE_ID, filter)
    results = response["results"]
    print(len(results))
    for result in results:
        weread = get_rich_text(result, "WeRead")
        title = get_title(result,"标题")
        id = result["id"]
        url = result["properties"]["条目链接"]["url"]
        get_read_ifo(weread,title,id,url)


def get_read_ifo(bookId,title,id,url):
    """获取书的详情"""
    session.get(WEREAD_BASE_URL)
    params = dict(bookId=bookId, readingDetail=1)
    r = session.get(WEREAD_HISTORY_URL,params=params)
    print(r.text)
    if r.ok:
        datas = r.json()["readDetail"]["data"]
        for data in datas:
            date = data["readDate"]
            date = datetime.fromtimestamp(date)
            minutes = floor(data["readTime"] / 60)
            page_id= query_database(bookId,date)
            if page_id =="":
                insert(title,id,minutes,url,date,bookId)
            else:
                update(page_id,minutes)


def query_database(weread,date):
    date = date.strftime("%Y-%m-%dT00:00:00+08:00")
    filter= {
        "and":[
        {"property": "ID", "rich_text": {"equals": weread}},
        {"property": "Date", "date": {"equals": date}},
        ]
    }
    id = ""
    response = notion_api.query_database("cca71ece15ac48a68c34e5f86a2e6b38", filter)
    results = response["results"]
    if len(results) > 0:
        id = results[0]["id"]
    return id 

def update(id,minutes):
    properties = (
        Properties()
        .number("时长", minutes)
    )
    notion_api.update_page(id,properties)

def insert(title, id,minutes,url,date,bookId):
    properties = (
        Properties()
        .title(title)
        .rich_text("ID",bookId)
        .relation("Book", id)
        .url("URL",url)
        .number("时长", minutes)
        .date(start=date.strftime("%Y-%m-%dT00:00:00"))
    )
    properties = notion_api.get_relation(properties,date=date)
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
    parser.add_argument("cookies")
    options = parser.parse_args()
    cookies = options.cookies
    session = requests.Session()
    session.cookies = parse_cookie_string(cookies)
    get_reading()