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
def createPage( pageId, cover):
    emo = "☀️"
    tomorrow = datetime.now()+timedelta(days=1)
    week = tomorrow.strftime("%V")
    month = tomorrow.month
  
    title = datetime.strftime(tomorrow,'%m月%d日 星期'+week_day_dict[tomorrow.weekday()])
    children = [{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}},
                        {"type": "heading_2", "heading_2": { "text": [{"type": "text", "text": {"content": "✅  TODO"}}]}},
                     ]
    for todo in getTodo():
        children.append(todo)
    children.append({"type": "heading_2", "heading_2": { "text": [{"type": "text", "text": {"content": "💬 碎碎念"}}]}})
    children.append({"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}})
    children.append({"type": "heading_2", "heading_2": { "text": [{"type": "text", "text": {"content": "📅 今日日程"}}]}})
    children.append({"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": ""}}]}})

    body = {"parent": { "database_id": pageId},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "日期": {"date": {"start": datetime.strftime(tomorrow,"%Y-%m-%d")}},
        "标签": {"type":"multi_select","multi_select":[{"name":str(month)+"月"},{"name":"第"+week+"周"}]},
    },
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": emo}, 
         "children": children
    }
    r = requests.post('https://api.notion.com/v1/pages/',headers=headers, json=body)
    print(r.text)

def getTodo():
    todo =[]
    tomorrow = datetime.now()+timedelta(days=1)
    day = tomorrow.day   
    week = tomorrow.weekday()
    print("day"+str(day))
    if(week < 10):
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"🍚 订餐"}}],"checked":False}})
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"💰 打新"}}],"checked":False}})
        if(week == 4):
            todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"💰 定投"}}],"checked":False}})
    if(day <32):
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"💳  信用卡还款"}}],"checked":False}})
    todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"🏃🏻 步数打卡"}, "link":{"url":"https://www.json.cn/"}}],"checked":False}})
    return todo

    
#获取封面
def getCover(accessKey, pageId):
    params = {"client_id": accessKey, "orientation": "landscape"}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    cover = r.json().get("urls").get("small")
    print(r.text)
    createPage( pageId, cover)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    headers = {'Authorization': options.secret, "Notion-Version": options.version}
    getCover(options.accessKey,options.id)
