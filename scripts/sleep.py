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

# 搜索笔记


def search(secret, version, content):
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime())
    headers = {'Authorization': secret, "Notion-Version": version}
    body = {"query": title}
    r = requests.post("https://api.notion.com/v1/search",
                      headers=headers, json=body)
    result = r.json().get("results")[0]
    id = result.get("id")
    updateDiary(secret, version, id, content)


def updateDiary(secret, version, pageId, content):
    content = json.loads(content)
    start = content['start']
    end = content['end']
    duration = content['duration']
    headers = {'Authorization': secret, "Notion-Version": version}
    body = {
        "properties": {
            "睡眠时长": {"number": float(duration)},
            "睡眠开始": {"rich_text": [{"type": "text", "text": {"content": start[start.find("午")+1:]}}]},
            "睡眠结束": {"rich_text": [{"type": "text", "text": {"content": end[end.find("午")+1:]}}]},
        }
    }
    r = requests.patch('https://api.notion.com/v1/pages/'+pageId,
                       headers=headers, json=body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("content")
    options = parser.parse_args()
    search(options.secret, options.version, options.content)
