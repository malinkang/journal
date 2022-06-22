#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import argparse
import time

from datetime import datetime

from requests.api import get


def getWeekDay():
    week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
    today = datetime.now().weekday()
    return week_day_dict[today]

# 搜索笔记
def search(content):
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime())
    body = {"query": title}
    r = requests.post("https://api.notion.com/v1/search",
                      headers=headers, json=body)
    result = r.json().get("results")[0]
    id = result.get("id")
    updateDiary( id, content)


def updateDiary(id, content):
    content = json.loads(content)
    start = content['start']
    end = content['end']
    duration = content['duration']
    print(start)
    print(end)
    startTime = start[start.find("午")+1:]
    endTime = end[end.find("午")+1:]
    
    body = {
        "properties": {
            "睡眠时长": {"number": float(duration)},
            "睡眠开始": {"rich_text": [{"type": "text", "text": {"content": startTime}}]},
            "睡眠结束": {"rich_text": [{"type": "text", "text": {"content":endTime }}]},
        }
    }
    r = requests.patch('https://api.notion.com/v1/pages/'+id,
                       headers=headers, json=body)
    content = startTime+"~"+endTime+" 睡觉"
    children = [
        {
        "type":"bulleted_list_item",
        "bulleted_list_item":{
            "text":[
                {
                    "type":"text",
                    "text":{
                        "content":content
                    }
                }
            ]
        }
    }
    ]
    getBlock(id,children)



def getBlock(id,children):
    r = requests.get('https://api.notion.com/v1/blocks/'+id,headers=headers)
    append(r.json().get('id'),children)

#添加block
def append(id,children):
    print(children)
    body = {
        "children":children
    }
    r = requests.patch('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers,json=body)
headers={}  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("content")
    options = parser.parse_args()
    headers = {'Authorization':options.secret, "Notion-Version":options.version}
    search(options.content)
