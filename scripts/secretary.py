#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
from typing import ItemsView
import requests
import os
import base64
import argparse
import time
import sys

from requests.api import get, post


def getCover(accessKey):
    params = {"client_id": accessKey, "orientation": "landscape"}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    cover = r.json().get("urls").get("small")
    search(cover)

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

def search(cover):
    body={"query":"今年"}
    now = datetime.now()
    title = now.strftime("%Y年%m月%d日")
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    properties = r.json().get("results")[0].get("properties")
    name = properties.get("Name").get("title")[0].get("text").get("content")
    content = properties.get("倒数日").get("formula").get("string")
    progress = properties.get("进度条").get("formula").get("string")
    message = title +"\n\n"
    message += name+content+"\n"
    message += progress+"\n\n"
    message +="今日待办:\n\n"
    index = 1
    day = now.day
    week = now.weekday()
    print(map[index])
    if(week < 5):
        message +=map[index]+" 订餐\n\n"
        index += 1
        message +=map[index]+" 打新\n\n"
        index += 1
    if(day == 6 or day == 8 or day == 21):
        message +=map[index]+" 信用卡还款\n\n"
    send(message,cover)
    print(cover)
    print(r.text)
    
#创建markdown文件
def send(message,cover):
    url = "https://api.telegram.org/bot1756944825:AAHVzM7zWJ-QTwomwTOJrF08raPqVqhtQhc/sendPhoto"
    print(message)
    body = {
        "chat_id": "@xiaoma1989",
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
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    headers = {'Authorization': options.secret,"Notion-Version":options.version}
    getCover( options.accessKey)
