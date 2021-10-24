#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import os
import base64
import argparse
import time
import sys

from datetime import datetime

from requests.api import get


def getWeekDay():
    week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
    today = datetime.now().weekday()
    return week_day_dict[today]


def createDiary(secret, pageId, version, cover):
    emo = "☀️"
    week = datetime.now().strftime("%V")
    month = datetime.now().month
    headers = {'Authorization': secret, "Notion-Version": version}
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime())
    body = {"parent": {"type": "database_id", "database_id": pageId},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "日期": {"date": {"start": time.strftime("%Y-%m-%d", time.localtime())}},
        "周": {"select": {"name": "第"+week+"周"}},
        "月": {"select": {"name": str(month)+"月"}},
    },
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": emo},
        "children": [{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}},
                     {"type": "heading_2", "heading_2": {
                         "text": [{"type": "text", "text": {"content": "每日任务"}}]}},
    
                     ]
    }
    r = requests.post('https://api.notion.com/v1/pages/',
                      headers=headers, json=body)


def getCover(accessKey, secret, pageId, version):
    params = {"client_id": accessKey, "orientation": "landscape"}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    cover = r.json().get("urls").get("full")
    createDiary(secret, pageId, version, cover)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    getCover(options.accessKey, options.secret,options.id, options.version)
