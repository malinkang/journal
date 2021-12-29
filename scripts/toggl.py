#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import ItemsView
import urllib.parse
import argparse
from datetime import date, datetime, timedelta, timezone
import requests
from requests.api import get
from requests.auth import HTTPBasicAuth


def createDiary():
    now = datetime.now()
    print(now)
    #前一天的11点半
    start = datetime(now.year,now.month,now.day-1,15,30).astimezone(tz=timezone(timedelta(hours=8)))
    start = start.replace(microsecond=0).isoformat()
    print("start = "+start)
    auth = ('2ef95512ce5b1528809f9a03a68e02b1', 'api_token')
    params = {'start_date':start}
    response = requests.get('https://api.track.toggl.com/api/v8/time_entries',params=params, auth=auth)
    print(response.text)
    print(response.request.url)
    message = ""
    for task in response.json():
        if task.get('pid') is not None and task.get('stop') is not None:
            newTags = []
            tags = task.get('tags')
            if tags is not None:
                for tag in tags:
                    newTag= {"name":tag}
                    newTags.append(newTag)
            start = datetime.strptime(task.get('start'),'%Y-%m-%dT%H:%M:%S%z').astimezone(tz=timezone(timedelta(hours=8)))
            start = start.replace(microsecond=0).isoformat()
            end = datetime.strptime(task.get('stop'),'%Y-%m-%dT%H:%M:%S%z').astimezone(tz=timezone(timedelta(hours=8)))
            end = end.replace(microsecond=0).isoformat()
            response = requests.get("https://api.track.toggl.com/api/v8/projects/"+str(task.get('pid')),auth=auth)
            name = response.json().get("data").get("name")
            message += name+""+"\n"
            print(newTags)
            emoji = name[0:1]
            description = ""
            if task.get("description") is not None:
                description = task.get("description")
            body = {"parent": {"type": "database_id", "database_id": "d8eee75d8c1049e7aa3dd6614907bb04"},
                    "properties": {
                "title": {"title": [{"type": "text", "text": {"content": name[1:]}}]},
                "开始": {"date": {"start": start}},
                "结束": {"date": {"start": end}},
                "备注": {"rich_text": [{"type": "text", "text": {"content":description }}]},
                "标签": {"multi_select":newTags},
                "分类": {"select":{"name":name}},

            },
                "icon": {"type": "emoji", "emoji": emoji},
            }
            r = requests.post('https://api.notion.com/v1/pages/',headers=headers, json=body)
    send(message)
#创建markdown文件
def send(message):
    url = "https://api.telegram.org/bot1756944825:AAHVzM7zWJ-QTwomwTOJrF08raPqVqhtQhc/sendPhoto"
    print(message)
    body = {
        "chat_id": "@xiaoma1989",
        "photo": "https://images.unsplash.com/photo-1640412751362-28febe09c3a3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=Mnw2ODUwfDB8MXxyYW5kb218fHx8fHx8fHwxNjQwNzc4ODA5&ixlib=rb-1.2.1&q=80&w=400",
        "caption":message,
        "parse_mode": "MarkdownV2"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.request("POST", url, headers=headers, json=body)
    print(r.text)
        
headers={}  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    options = parser.parse_args()
    headers = {'Authorization': options.secret, "Notion-Version":options.version}
    createDiary()