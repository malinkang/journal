#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
from audioop import add
from calendar import week
from curses import noecho
from dis import dis
from operator import truediv
import time
import requests
from datetime import date, datetime, timedelta, timezone
LOGIN_API = "https://api.gotokeep.com/v1.1/users/login"
RUN_DATA_API = "https://api.gotokeep.com/pd/v3/stats/detail?dateUnit=all&type=running&lastDate={last_date}"
RUN_LOG_API = "https://api.gotokeep.com/pd/v3/runninglog/{run_id}"



def login( mobile, passowrd):
    data = {"mobile": mobile, "password": passowrd}
    r = requests.post(LOGIN_API, headers=keep_headers, data=data)
    if r.ok:
        token = r.json()["data"]["token"]
        keep_headers["Authorization"] = f"Bearer {token}"
        get_run_id()

def get_run_id():
    last_date=0
    r = requests.get(RUN_DATA_API.format(last_date=last_date), headers=keep_headers)
    if r.ok:
        last_date = r.json()["data"]["lastTimestamp"]
        for record in filter(is_today,r.json().get("data").get("records")):
            for log in record.get("logs"):
                id = log.get("stats").get("id")
                get_run_data(id,record.get("date"))
def is_today(record):
    today = (datetime.now()-timedelta(days=1)).strftime("%-m月%d日")
    return today == record.get("date")
               
def get_run_data(id,title):
    r = requests.get(RUN_LOG_API.format(run_id=id), headers=keep_headers)
    if r.ok:
        data = r.json().get("data")
        start = datetime.fromtimestamp(data.get("startTime")/1000).astimezone(tz=timezone(timedelta(hours=8)))
        week = "第"+start.strftime("%-V")+"周"
        year = start.strftime("%Y")
        start = start.replace(microsecond=0).isoformat()
        end = datetime.fromtimestamp(data.get("endTime")/1000).astimezone(tz=timezone(timedelta(hours=8)))
        end = end.replace(microsecond=0).isoformat()
        cover = data.get("polylineSnapshot")
        if cover is None:
            cover = "https://images.unsplash.com/photo-1502224562085-639556652f33?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=6000"
        distance = round(float(data.get("distance"))/1000,2)
        add_to_notion(start,end,cover,distance,title,week,year)
def add_to_notion(start,end,cover,distance,title,week,year):
    week = search_week(week,year)
    body = {"parent": { "database_id": "8dc2c4145901403ea9c4fb0b10ad3f86"},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "时间": {"date": {"start": start,"end":end}},
        "距离": {"number":distance },
        "周": {
            "relation": [
                    {
                        "id": week,
                    }
                ]
            }
        },
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": "🏃🏻"}, 
    }
    r = requests.post('https://api.notion.com/v1/pages/',headers=notion_headers, json=body)
    print(r.text)

def search_week(week,year):
    year = search_year(year)
    body = {
    "filter": {
        "and": [
            {
                "property": "Name",
                "text":{
                    "equals":week
                }
            },
            {
                "property": "年",
                "relation": {
                    "contains":year
                }
            }
        ]
    }
}
    r = requests.post("https://api.notion.com/v1/databases/194f66886cd8479899d38b0fb0b7da26/query",headers=notion_headers,json=body)
    return r.json().get("results")[0].get("id")

#获取年的datebase_id
def search_year(year):
    body = {
    "filter": {
        "and": [
            {
                "property": "Name",
                "text":{
                    "equals":year
                }
            }
        ]
        }
    }
    r = requests.post("https://api.notion.com/v1/databases/f4d2374344ca409aa22d40e8d33833eb/query",headers=notion_headers,json=body)
    return r.json().get("results")[0].get("id")

def create_week():
    #第一周的开始时间
    start = datetime(year=2022,month=1,day=3,hour=0,minute=0,second=0,microsecond=0)
    for i in range(1,52):
        week_start = start + timedelta(days=7*i)
        week = "第"+str(i+1)+"周"
        week_end = week_start + timedelta(days=6)
        print("start ="+week_start.astimezone(tz=timezone(timedelta(hours=8))).isoformat())
        print("end ="+week_end.astimezone(tz=timezone(timedelta(hours=8))).isoformat())
        create_week_item(week_start.astimezone(tz=timezone(timedelta(hours=8))).isoformat(),week_end.astimezone(tz=timezone(timedelta(hours=8))).isoformat(),week)


## 创建周        

def create_week_item(start,end,title):
    body = {"parent": { "database_id": "194f66886cd8479899d38b0fb0b7da26"},
            "properties": {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "时间": {"date": {"start": start,"end":end}},
        "年": {
            "relation": [
                    {
                        "id": "c26c09e0-dfff-4918-b0b1-c04a3fac4964",
                    }
                ]
            }
        },
        "cover": {"type": "external", "external": {"url": getCover()}},
        "icon": {"type": "emoji", "emoji": "🌿"}, 
    }
    r = requests.post('https://api.notion.com/v1/pages/',headers=notion_headers, json=body)
    print(r.text)

def getCover():
    params = {"client_id": "cXKRBgzoILHbD1OhNZs3f5hiZBFJWSrp3K1NiA2XGeM", "orientation": "landscape"}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    cover = r.json().get("urls").get("small")
    return cover
keep_headers  = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
}
notion_headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phone_number")
    parser.add_argument("password")
    parser.add_argument("notion_secret")
    parser.add_argument("notion_version")
    options = parser.parse_args()
    print("执行时间"+datetime.now().isoformat())
    notion_headers = {'Authorization':options.notion_secret, "Notion-Version": options.notion_version}
    login(options.phone_number, options.password) 