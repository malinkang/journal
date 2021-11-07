#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, datetime
import json
import requests
import os
import base64
import argparse
import time
import sys

from datetime import datetime,timedelta

from requests.api import get


week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}


#创建Page
def createPage(secret, pageId, version, cover):
    emo = "☀️"
    tomorrow = datetime.now()+timedelta(days=1)
    week = tomorrow.strftime("%V")
    month = tomorrow.month
    headers = {'Authorization': secret, "Notion-Version": version}
    title = datetime.strftime(tomorrow,'%m月%d日 星期'+week_day_dict[tomorrow.weekday()])
    body = {"parent": { "database_id": pageId},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "日期": {"date": {"start": datetime.strftime(tomorrow,"%Y-%m-%d")}},
        "标签": {"type":"multi_select","multi_select":[{"name":str(month)+"月"},{"name":"第"+week+"周"}]},
    },
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": emo}, 
         "children": [{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}},
                     {"type": "heading_2", "heading_2": { "text": [{"type": "text", "text": {"content": "💬 碎碎念"}}]}},
                     {"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}},
                     {"type": "heading_2", "heading_2": { "text": [{"type": "text", "text": {"content": "📅 今日日程"}}]}},
                    {"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}},
                     ]
    }
    r = requests.post('https://api.notion.com/v1/pages/',headers=headers, json=body)
    print(r.text)
#创建Database
def createDatabase(secret, pageId, version):
    headers = {'Authorization': secret, "Notion-Version": version}
    body = {"parent": {"type": "page_id", "page_id": pageId},
      
    }
    r = requests.post('https://api.notion.com/v1/databases/',headers=headers, json=body)
    print(r.text)
#获取封面
def getCover(accessKey, secret, pageId, version):
    params = {"client_id": accessKey, "orientation": "landscape"}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    cover = r.json().get("urls").get("small")
    print(r.text)
    createPage(secret, pageId, version, cover)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    getCover(options.accessKey, options.secret,options.id, options.version)
