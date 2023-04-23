

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
WEREAD_NOTE_URL = "https://i.weread.qq.com/shelf/sync"
WEREAD_HOT_URL = "https://i.weread.qq.com/book/bestbookmarks"

"""
https://i.weread.qq.com/readdata/detail?mode=weekly&baseTime=0
https://i.weread.qq.com/readdata/detail?mode=monthly&baseTime=0
https://i.weread.qq.com/readdata/detail?mode=anually&baseTime=0
https://i.weread.qq.com/readdata/detail?mode=overall&baseTime=0
"""


def get_weekly_reading():
    """
    获取周阅读数据
    """
    params = dict(mode="weekly", baseTime=0)
    r = session.get("https://i.weread.qq.com/readdata/detail", params=params)
    if r.ok and "readTimes" in r.json():
        readTimes = r.json()["readTimes"]
        for key,value in readTimes.items():
            page_id = query_read_times(key)
            if(page_id!=""):
                update_read_time(page_id,value)
            else:
                insert_read_times(key,value,datetime.fromtimestamp(int(key)) )
def query_read_times(timestamp):
    filter = {
        "and": [
            {"property": "Timestamp", "title": {"equals": timestamp}},
        ]
    }
    id = ""
    response = notion_api.query_database(
        "09aadf6940c74beb81baf3d60121c7a2", filter)
    results = response["results"]
    if len(results) > 0:
        id = results[0]["id"]
    return id


def update_read_time(id, minutes):
    properties = (
        Properties()
        .number("Minutes", minutes)
    )
    notion_api.update_page(id, properties)

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


def get_reading(weread):
    """
    从Database中获取某本书的id和url
    """
    filter =  {"property": "WeRead", "rich_text": {"equals": weread}}
    response = notion_api.query_database(BOOK_DATABASE_ID, filter)
    results = response["results"]
    for result in results:
        title = get_title(result, "标题")
        id = result["id"]
        url = result["properties"]["条目链接"]["url"]
        get_read_ifo(weread, title, id, url)

def insert_read_times(title,  minutes, date):
    properties = (
        Properties()
        .title(title)
        .number("Minutes", minutes)
        .date(start=date.strftime("%Y-%m-%dT00:00:00"))
    )
    properties = notion_api.get_relation(properties, date=date)
    page = (
        Page()
        .parent(DatabaseParent("09aadf6940c74beb81baf3d60121c7a2"))
        .children(Children())
        .properties(properties)
        .cover(unsplash.random())
        .icon("📚")
    )
    notion_api.create_page(page)

def get_read_ifo(bookId, title, id, url):
    """
    https://i.weread.qq.com/book/readinfo?noteCount=1&readingDetail=1&readingBookIndex=1&finishedBookIndex=1&readingBookCount=1&finishedBookCount=1&bookId=44026191&finishedDate=1
    """
    params = dict(bookId=bookId, readingDetail=1,readingBookIndex=1)
    r = session.get(WEREAD_HISTORY_URL, params=params)
    print(r.text)
    if r.ok and  "readDetail" in r.json():
        datas = r.json()["readDetail"]["data"]
        for data in datas:
            date = data["readDate"]
            date = datetime.fromtimestamp(date) 
            if(date >=today):
                minutes = floor(data["readTime"] / 60)
                page_id = query_database(bookId, date)
                if page_id == "":
                    insert(title, id, minutes, url, date, bookId)
                else:
                    update(page_id, minutes)


def get_note(bookId):
    """获取划线"""
    session.get(WEREAD_BASE_URL)
    params = dict(bookId=bookId)
    r = session.get("https://i.weread.qq.com/book/bookmarklist", params=params)
    with open("note.json", "w") as f:
        json.dump(r.json(), f)


def get_hot(bookId):
    """获取热门划线"""
    session.get(WEREAD_BASE_URL)
    params = dict(bookId=bookId)
    r = session.get(WEREAD_HOT_URL, params=params)
    with open("note2.json", "w") as f:
        json.dump(r.json(), f)


def get_hot2(bookId):
    """获取笔记"""
    session.get(WEREAD_BASE_URL)
    params = dict(bookId=bookId, listType=11, mine=1, syncKey=0)
    r = session.get("https://i.weread.qq.com/review/list", params=params)
    with open("note2.json", "w") as f:
        json.dump(r.json(), f)

def get_notebooklist():
    """获取笔记本列表"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = session.get(url)
    books = []
    with open("notebooks.json", "w", encoding="utf-8") as f:
        f.write(r.text)
    if r.ok:
        data = r.json()
        for b in data["books"]:
            if today < datetime.fromtimestamp(b["sort"]):
                books.append(b["bookId"])
    return books

def query_database(weread, date):
    date = date.strftime("%Y-%m-%dT00:00:00+08:00")
    filter = {
        "and": [
            {"property": "ID", "rich_text": {"equals": weread}},
            {"property": "Date", "date": {"equals": date}},
        ]
    }
    id = ""
    response = notion_api.query_database(
        "cca71ece15ac48a68c34e5f86a2e6b38", filter)
    results = response["results"]
    if len(results) > 0:
        id = results[0]["id"]
    return id


def update(id, minutes):
    properties = (
        Properties()
        .number("时长", minutes)
    )
    notion_api.update_page(id, properties)


def insert(title, id, minutes, url, date, bookId):
    properties = (
        Properties()
        .title(title)
        .rich_text("ID", bookId)
        .relation("Book", id)
        .url("URL", url)
        .number("时长", minutes)
        .date(start=date.strftime("%Y-%m-%dT00:00:00"))
    )
    properties = notion_api.get_relation(properties, date=date)
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
    session.get(WEREAD_BASE_URL)
    today = datetime.now()
    today = today.replace(hour=0,minute=0, second=0, microsecond=0)
    books = get_notebooklist()
    for book in books:
        get_reading(book)
    get_weekly_reading()