# -*- coding: utf-8 -*-
#!/usr/bin/python

from datetime import datetime, timedelta, timezone
import json
from unittest import result
import unsplash
import requests
import notion
import date


FOREST_URL_HEAD = "https://forest-china.upwardsware.com"
FOREST_LOGIN_URL = FOREST_URL_HEAD + "/api/v1/sessions"
FOREST_CLAENDAR_URL = (
    FOREST_URL_HEAD
    + "/api/v1/plants/updated_plants?update_since={date}&seekruid={user_id}"
)
TODO = "88a6a9b5b15a45fd8e97a56cb0d30763"
TOMATO = "bcdcfb9068eb458a94c8266c2b88ec09"
FOREST_TAG_URL = FOREST_URL_HEAD + "/api/v1/tags?seekruid={id}"
email = "linkang.ma@gmail.com"
password = "FFitness06"
headers = {"Content-Type": "application/json"}
s = requests.Session()

#TODO 如果不存在TODO 创建一个TODO 
#TODO 获取PID
# 登录forest
def login():
    data = {"session": {"email": email, "password": password}}
    r = s.post(FOREST_LOGIN_URL, headers=headers, json=data)
    user_id = r.json().get("user_id")
    get_plants(user_id)


# 获取植物
def get_plants(user_id):
    now = datetime.now().strftime("%Y-%m-%d")
    r = s.get(
        FOREST_CLAENDAR_URL.format(date=now, user_id=user_id), headers=headers
    )
    for plant in r.json().get("plants"):
        note = plant.get("note")
        start_time = plant.get("start_time")
        end_time = plant.get("end_time")
        start = date.format_utc(start_time)
        end = date.format_utc(end_time)
        insert_notion(note, start, end,start_time,end_time)
    update_todo()

# 搜索todo
def search_todo(title):
    return notion.search(TODO, title)


# 番茄钟插入notion
def insert_notion(note, start, end,start_time,end_time):
    print("insert")
    properties = {
        "title": {"title": [{"type": "text", "text": {"content": note}}]},
        "时间": {"date": {"start": start, "end": end}},
         "start": {"rich_text": [{"type": "text", "text": {"content": start_time}}]},
        "end": {"rich_text": [{"type": "text", "text": {"content": end_time}}]},
    }
    properties = notion.get_relation(properties)
    properties["TODO"] = {"relation": [{"id": search_todo(note)}]}
    body = {
        "parent": {"database_id": TOMATO},
        "properties": properties,
        "cover": {"type": "external", "external": {"url": unsplash.random()}},
        "icon": {"type": "emoji", "emoji": "🍅"},
    }
    r = requests.post(
        "https://api.notion.com/v1/pages/", headers=notion.headers, json=body
    )
    


# 更新todo的时间
def update_todo():
    body = {
        "filter": {
            "and": [
                {"property": "时间", "date": {"is_empty": True}},
                {"property": "🍅", "rollup": {"number": {"greater_than": 0}}},
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/" + TODO + "/query",
        headers=notion.headers,
        json=body,
    )
    for result in r.json().get("results"):
        id = result.get("id")
        print(id)
        properties = result.get("properties")
        title = (
            properties.get("Name")
            .get("title")[0]
            .get("text")
            .get("content")
        )
        ret = get_end_time(title)
        print(ret)
        body = {
            "properties": {
                "时间": {"date": {"start": ret.get("start"), "end":ret.get("end")}}
            }
        }
        r = requests.patch(
            "https://api.notion.com/v1/pages/" + id, headers=notion.headers, json=body
        )
        print(r.text)
        duration = r.json().get("properties").get("duration").get("formula").get("number")
    insert_to_toggl(title, ret.get("start_time"), duration,"177393358")

# 插入Toggle
def insert_to_toggl(description, start, duration,pid):
    print("toggl")
    auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")
    params = {"time_entry":{"description":description,"start": start, "duration": duration, "pid": pid,"created_with":"curl"}}
    response = requests.post(
        "https://api.track.toggl.com/api/v8/time_entries", json=params, auth=auth,headers=headers
    )
    print(response.text)


def get_end_time(title):
    body = {
        "filter": {"and": [{"property": "Name", "text": {"equals": title}}]},
        "sorts": [{"property": "时间", "direction": "ascending"}],
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/" + TOMATO + "/query",
        headers=notion.headers,
        json=body,
    )
    results = r.json().get("results")
    size = len(results)
    start = results[0].get("properties").get("时间").get("date").get("start")
    end = results[size - 1].get("properties").get("时间").get("date").get("end")
    start_time = results[0].get("properties").get("start").get("rich_text")[0].get("text").get("content")
    return {"start": start, "end": end,"start_time":start_time}


if __name__ == "__main__":
    login()