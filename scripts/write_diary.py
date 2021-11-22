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
import csv

from datetime import datetime

from requests.api import get

def getWeekDay():
    week_day_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    today = datetime.now().weekday()
    return week_day_dict[today]

def createDiary(title,startTime,endTime):
    body = {"parent": {"type": "database_id", "database_id": "101341b8f9634e7a9ad522103db35731"},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "时间": {"date": {"start": startTime,"end":endTime}},
    },
        "icon": {"type": "emoji", "emoji": "😄"},
    }
    r = requests.post('https://api.notion.com/v1/pages/',headers=headers, json=body)
    print(r.text)


def getEvent():
    date =time.strftime("%Y-%m-%d", time.localtime()) 
    body = {
    "filter": {
        "or": [
            {
                "property": "日期",
                "date":{
                    "equals":date
                }
            }
        ]
    },
    "sorts": [
        {
        "property": "日期",
        "direction": "ascending"
            }
        ]
    }
    r = requests.post("https://api.notion.com/v1/databases/d8eee75d8c1049e7aa3dd6614907bb04/query",headers=headers,json=body)
    results = r.json().get("results");
    list = []
    for result in results:
        properties = result.get("properties");
        name = properties.get("Name").get("title")[0].get("text").get("content")
        if(properties.get("备注") is not None and len(properties.get("备注").get("rich_text"))>0):
            name = properties.get("备注").get("rich_text")[0].get("text").get("content")
        startTime = properties.get("时间").get("date").get("start")
        endTime = properties.get("时间").get("date").get("end")
        print(name)
        start = datetime.strftime(datetime.strptime(startTime,"%Y-%m-%dT%H:%M:%S.000+00:00"),"%H:%M")
        end = datetime.strftime(datetime.strptime(endTime,"%Y-%m-%dT%H:%M:%S.000+00:00"),"%H:%M")
        content = start+"~"+end+" "+name
        body = {
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
                
        list.append(body)
    search(list)

#解析csv
def parseCsv():
    file = time.strftime('%Y%m%d', time.localtime())
    filename = "./data/"+file+".csv"
    with open(filename) as f:
        render = csv.reader(f)
        header_row = next(render)
        print(header_row) 
        list = []
        for row in render:
            startTime = row[0]
            start = datetime.strptime(startTime,"%Y-%m-%dT%H:%M:%S.%f+0800")
            #获取今日0点
            now = datetime.now()
            zero = datetime(now.year,now.month,now.day,0,0)
            if(start > zero):
                endTime = row[1]
                end = datetime.strftime(datetime.strptime(endTime,"%Y-%m-%dT%H:%M:%S.%f+0800"),"%H:%M")
                start = datetime.strftime(start,"%H:%M")
                tag = row[2]
                note = row[3]
                title = ""
                if(len(note)==0):
                    title = tag
                else:
                    title = note
                content = start+"~"+end+" "+title
                body = {
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
                list.append(body)
        # print(list)
        search(list)
    #     createDiary(title,startTime,endTime)

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
    print(r.text)

#搜索需要同步的笔记
def search(children):
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime()) 
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    result = r.json().get("results")[0]
    id = result.get("id")
    getBlock(id,children)
    
headers={}  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    options = parser.parse_args()
    headers = {'Authorization': options.secret, "Notion-Version":options.version}
    getEvent()
