#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
from dataclasses import dataclass
import json
import unsplash
import notion
import dateutils
from datetime import datetime, timedelta
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
from notion_api import Children
import notion_api
import requests



# 搜索笔记
def insert(content):
    content = json.loads(content)
    start = format_date(content["start"],True)
    end = format_date(content["end"])
    insert_to_notion(start,end)
    insert_to_toggl("AutoSleep自动同步",start,(end-start).seconds,"177393271")

def format_date(d,start=False):
    date = d[: d.find("周")] + " " + d[d.find("午") + 1 :]
    date = datetime.strptime(date, "%y/%m/%d %H:%M")
    print(date.hour)
    if "下午" in d:
        date +=timedelta(hours=12)
    #autosleep上午0点不是0点是12点，所以如果是12点，那么就要减去12小时
    if start and date.hour ==12:
        date -= timedelta(hours=12)
    return date
# 插入Toggle
def insert_to_toggl(description, start, duration,pid):
    start = start - timedelta(hours=8)
    auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")
    params = {"time_entry":{"description":description,"start": start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "duration": duration, "pid": pid,"created_with":"curl"}}
    response = requests.post(
        "https://api.track.toggl.com/api/v8/time_entries", json=params, auth=auth
    )
    print(response.text)

def insert_to_notion(start,end):
    now = datetime.now()
    title = dateutils.format_date_with_week(date=now)
    cover = unsplash.random()
    properties = Properties().title(title).date("睡眠",start,end)
    properties = notion_api.get_relation(properties,now,False)
    parent = DatabaseParent("8117b5547c7b44f5a3cb0fdfb2b464e4")
    page  = Page().parent(parent).children(Children()).cover(cover).icon("😴").properties(properties)
    notion_api.create_page(page=page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    insert(options.content)
