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


def emoji(weather):
    if("晴" in weather):
        return "☀️"
    elif("雨" in weather):
        return "🌧"
    elif("雪" in weather):
        return "❄️"
    elif("云" in weather):
        return "☁️"
    elif("雾" in weather):
        return "🌫"
    else:
        return "☀️"


def createDiary(secret, pageId, version, cover, content):
    content = json.loads(content)
    weight = content['weight']
    weather = content['weather']
    highest = content['highest']
    lowest = content['lowest']
    start = content['start']
    end = content['end']
    duration = content['duration']
    aqi = content['aqi']
    location = content['location']
    emo = emoji(weather)
    startTime = start[0:start.find("周")]+" "+start[start.find("午")+1:]
    endTime = end[0:start.find("周")]+" "+end[start.find("午")+1:]
    time.strptime(startTime, "%y/%m/%d %H:%M")
    time.strptime(endTime, "%y/%m/%d %H:%M")
    startTime = time.strftime(
        "%Y-%m-%dT%l:%M:%S.000+08:00", time.strptime(startTime, "%y/%m/%d %H:%M"))
    endTime = time.strftime("%Y-%m-%dT%l:%M:%S.000+08:00",
                            time.strptime(endTime, "%y/%m/%d %H:%M"))
    headers = {'Authorization': secret, "Notion-Version": version}
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime())
    body = {"parent": {"type": "database_id", "database_id": pageId},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        # "体重": {"number": weight},
        # "空气质量": {"number": aqi},
        # "最高温度": {"rich_text": [{"type": "text", "text": {"content": highest}}]},
        # "最低温度": {"rich_text": [{"type": "text", "text": {"content": lowest}}]},
        # "天气": {"rich_text": [{"type": "text", "text": {"content": weather}}]},
        # "位置": {"rich_text": [{"type": "text", "text": {"content": location}}]},
        # "睡眠时间": {"date": {"start": startTime, "end": endTime}},
    },
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": emo},
        "children": [{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": content}}]}},
                     {"type": "heading_2", "heading_2": {
                         "text": [{"type": "text", "text": {"content": "每日任务"}}]}},
                     {"object": "block", "type": "to_do", "to_do": {
                         "text": [{"type": "text", "text": {"content": "1️⃣蚂蚁庄园养一颗🥚"}}], "checked": False}},
                     {"object": "block", "type": "to_do", "to_do": {
                         "text": [{"type": "text", "text": {"content": "2️⃣蚂蚁森林收集1kg能量"}}], "checked": False}},
                     {"object": "block", "type": "to_do", "to_do": {
                         "text": [{"type": "text", "text": {"content": "3️⃣走15000步"}}], "checked": False}},
                     {"object": "block", "type": "to_do", "to_do": {
                         "text": [{"type": "text", "text": {"content": "4️⃣记账"}}], "checked": False}},
                     ]
    }
    print(json.dumps(body))
    r = requests.post('https://api.notion.com/v1/pages/',
                      headers=headers, json=body)
    print(r.text)


def getCover(accessKey, secret, pageId, version, content):
    # params = {"client_id": accessKey, "orientation": "landscape"}
    # r = requests.get('https://api.unsplash.com/photos/random', params=params)
    # cover = r.json().get("urls").get("full")
    print("content")
    createDiary(secret, pageId, version, "", content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    parser.add_argument("content")
    options = parser.parse_args()
    getCover(options.accessKey, options.secret,
             options.id, options.version, options.content)
