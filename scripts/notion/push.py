#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cgitb import text
from datetime import datetime, timedelta
import requests
import argparse

import notion_api
import dateutils
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties


map = {
    1:"1️⃣",
    2:"2️⃣",
    3:"3️⃣",
    4:"4️⃣",
    5:"5️⃣",
    6:"6️⃣",
    7:"7️⃣",
    8:"8️⃣",
    9:"9️⃣",
    10:"🔟",
}
#获取星期
#搜索需要同步的笔记
def query_todo():
    yesterday = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%dT00:00:00+08:00")
    filter = {"and":[
        {"property": "Date", "date": {"after": yesterday}},
        {"property": "Status", "select": {"equals": "Not Started"}}
    ]}
    response = notion_api.query_database("97955f34653b4658bc0aaa50423be45f", filter)
    results= response.get("results")
    message = ""
    index = 0
    for result in results:
        index +=1
        message +=map[index]+" "+result['properties']['Name']['title'][0]['text']['content']
        message +="\n"
    send(message,"http://diary.malinkang.com/images/weread.svg")
    
    
#创建markdown文件
def send(message,cover):
    url = "https://api.telegram.org/bot5509900379:AAHSimr7FiKrclApJImy91A3Dff4R4g2OPk/sendPhoto"
    body = {
        "chat_id": "902643712",
        "photo": cover,
        "caption":message,
        "parse_mode": "MarkdownV2"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.request("POST", url, headers=headers, json=body)
    print(r.text)
   

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    query_todo()
