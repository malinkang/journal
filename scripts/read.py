#!/usr/bin/python
# -*- coding: UTF-8 -*-
from calendar import week
from datetime import date, datetime, timedelta, timezone
import json
import requests
import os
import base64
import argparse
import time
import sys
import csv
import notion

from datetime import datetime

from requests.api import get


# 1.获取正在读的书籍


def get_reading(end):
    body = {"filter": {"and": [{"property": "状态", "select": {"equals": "在读"}}]}}
    r = requests.post(
        "https://api.notion.com/v1/databases/c7efdba75f4146ad84a3f5b773998859/query",
        headers=headers,
        json=body,
    )
    result = r.json().get("results")[0]
    id = result.get("id")
    name = result.get("properties").get("标题").get("title")[0].get("text").get("content")
    start = get_yestorday(id)
    add(name, id, start, end)


def add(
    title,
    id,
    start,
    end,
):
    now = datetime.now()
    print(id)
    properties = {
            "Name": {"title": [{"type": "text", "text": {"content": title}}]},
            "书名": {
                "relation": [
                    {
                        "id": id,
                    }
                ]
            },
            "时间": {"date": {"start": now.strftime("%Y-%m-%d")}},
            "结束": {"number": int(end)},
            "开始": {"number": int(start)},
        }
    properties = notion.get_relation(properties)
    body = {
        "parent": {
            "type": "database_id",
            "database_id": "cca71ece15ac48a68c34e5f86a2e6b38",
        },
        "properties": properties,
        "icon": {"type": "emoji", "emoji": "📚"},
    }
    r = requests.post("https://api.notion.com/v1/pages/", headers=headers, json=body)





# 获取昨天的数据
def get_yestorday(id):
    body = {
        "filter": {"and": [{"property": "书名", "relation": {"contains": id}}]},
        "sorts": [{"property": "时间", "direction": "descending"}],
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/cca71ece15ac48a68c34e5f86a2e6b38/query",
        headers=headers,
        json=body,
    )
    results = r.json().get("results")
    page = 0
    if len(results) > 0:
        page = results[0].get("properties").get("结束").get("number")
    return page


headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("end")
    options = parser.parse_args()
    headers = {"Authorization": options.secret, "Notion-Version": options.version}
    get_reading(options.end)
