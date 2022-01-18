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
    'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'
    print(r.text)

def getTodo():
    todo =[]
    tomorrow = datetime.now()+timedelta(days=1)
    day = tomorrow.day   
    week = tomorrow.weekday()
    print("day"+str(day))
    leetcode(todo)
    android(todo)
    if(week < 5):
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"🍚 订餐","link":{"url":"https://meican.com/"}}}],"checked":False}})
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"💰 打新"}}],"checked":False}})
        if(week == 4):
            todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"💰 定投"}}],"checked":False}})
    if(day == 8 or day ==6  or day ==21):
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"💳  信用卡还款"}}],"checked":False}})
    todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"🏃🏻 步数打卡"}}],"checked":False}})
    return todo

def leetcode(todo):
    now = datetime.now()
    tomorrow = datetime(now.year,now.month,now.day+1,0,0)
    date =tomorrow.isoformat()
    print(tomorrow)
    body = {
    "filter": {
        "or": [
            {
                "property": "Date",
                "date":{
                    "equals":date
                }
            }
        ]
    },
    "sorts": [
        {
        "property": "Date",
        "direction": "ascending"
            }
        ]
    }
    r = requests.post("https://api.notion.com/v1/databases/b6f37ca9b5f844b487ac9c06e4813406/query",headers=headers,json=body)
    results = r.json().get("results")
    for result in results:
        properties = result.get("properties")
        title = properties.get("Title").get("title")[0].get("text").get("content")
        url = properties.get("url").get("rich_text")[0].get("href")
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":title,"link":{"url":url}}}],"checked":False}})

def android(todo):
    now = datetime.now()
    tomorrow = datetime(now.year,now.month,now.day+1,0,0)
    date =tomorrow.isoformat()
    print(tomorrow)
    body = {
    "filter": {
        "or": [
            {
                "property": "学习时间",
                "date":{
                    "equals":date
                }
            }
        ]
    },
    "sorts": [
        {
        "property": "Date",
        "direction": "ascending"
            }
        ]
    }
    r = requests.post("https://api.notion.com/v1/databases/48fa2b28ce294476b12046589ac33663/query",headers=headers,json=body)
    print(r.text)
    results = r.json().get("results")
    for result in results:
        properties = result.get("properties")
        title = properties.get("Title").get("title")[0].get("text").get("content")
        url = result.get("url")
        todo.append({"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":title,"link":{"url":url}}}],"checked":False}})
#获取封面
def getCover(accessKey, pageId):
    params = {"client_id": accessKey, "orientation": "landscape"}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    cover = r.json().get("urls").get("small")
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
