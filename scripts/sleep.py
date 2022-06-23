#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
import json
import requests
import argparse
import time
from notion import Properties
import notion
import dateutils

from datetime import datetime

from requests.api import get


def getWeekDay():
    week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
    today = datetime.now().weekday()
    return week_day_dict[today]


# 搜索笔记
def search(content):
    title = dateutils.format_date_with_week()
    print(title)
    body = {
        "filter": {"and": [{"property": "标题", "text": {"equals": title}}]},
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/294060cde13e4c29b0ac6ee490c8a448/query",
        headers=notion.headers,
        json=body,
    )
    result = r.json().get("results")[0]
    id = result.get("id")
    content = json.loads(content)
    start = format_date(content["start"])
    end = format_date(content["end"])
    insert_to_notion(id, start,end)
    insert_to_toggl("AutoSleep自动同步",start,(end-start).seconds,"177393271")

def format_date(d):
    date = d[: d.find("周")] + " " + d[d.find("午") + 1 :]
    if "上午" in d:
        date = datetime.strptime(date, "%y/%m/%d %I:%M")
    else:
        date = datetime.strptime(date, "%y/%m/%d %H:%M")
    return date
# 插入Toggle
def insert_to_toggl(description, start, duration,pid):
    start = start - timedelta(hours=8)
    auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")
    params = {"time_entry":{"description":description,"start": start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "duration": duration, "pid": pid,"created_with":"curl"}}
    response = requests.post(
        "https://api.track.toggl.com/api/v8/time_entries", json=params, auth=auth,headers=headers
    )
    print(response.text)

def insert_to_notion(id, start,end):
    properties = Properties().date("睡眠", start.isoformat(),end.isoformat() )
    properties = {"properties": properties}
    print(properties)
    r = requests.patch(
        "https://api.notion.com/v1/pages/" + id, headers=headers, json=properties
    )
    print(r.text)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("content")
    options = parser.parse_args()
    headers = {'Authorization': options.secret,"Notion-Version":options.version}
    search(options.content)
