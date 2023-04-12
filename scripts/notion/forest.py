# -*- coding: utf-8 -*-
#!/usr/bin/python

from datetime import datetime, timedelta
import json
import unsplash
import requests
import notion
import date
import dateutils
from notion_api import Properties
from notion_api import Page
import notion_api
from notion_api import DatabaseParent
from notion_api import Children
from config import TOMATO_DATABASE_ID
import util
FOREST_URL_HEAD = "https://forest-china.upwardsware.com"
FOREST_LOGIN_URL = FOREST_URL_HEAD + "/api/v1/sessions"
FOREST_CLAENDAR_URL = (
    FOREST_URL_HEAD
    + "/api/v1/plants/updated_plants?update_since={date}&seekruid={user_id}"
)
TODO = "97955f34653b4658bc0aaa50423be45f"
FOREST_TAG_URL = FOREST_URL_HEAD + "/api/v1/tags?seekruid={id}"
email = "linkang.ma@gmail.com"
password = "FFitness06"
headers = {"Content-Type": "application/json"}
USER_ID = "6d411501-82d6-46e5-b809-97c0fdce722c"
s = requests.Session()

dict = {
    15: "👨‍💻工作",  # 工作
    50: "📚读书",  # 计算机网络原理
    51: "🍎LeetCode",  # 计算机网络原理
    52: "🌐计算机网络原理",  # 计算机网络原理
    53: "🇺🇸英语",  # 计算机网络原理
}

dict2 = {
    "👨‍💻工作":177393358,  # 工作
    "📚读书":177394096,  # 计算机网络原理
    "🍎LeetCode":188371890,  # 计算机网络原理
    "🌐计算机网络原理":189166678,  # 计算机网络原理
    "🇺🇸英语":186296615,  # 计算机网络原理
}

def login():
    data = {"session": {"email": email, "password": password}}
    r = s.post(FOREST_LOGIN_URL, headers=headers, json=data)
    user_id = r.json().get("user_id")
    return user_id


def get_plants(user_id):
    now = datetime.now().strftime("%Y-%m-%d")
    r = s.get(FOREST_CLAENDAR_URL.format(
        date=now, user_id=user_id), headers=headers)
    plants = r.json().get("plants")
    for plant in plants:
        id = plant.get("id")
        tag = plant.get("tag")
        note = plant.get("note").strip()
        start_time = plant.get("start_time")
        end_time = plant.get("end_time")
        start = date.format_utc(start_time) + timedelta(hours=8)
        end = date.format_utc(end_time) + timedelta(hours=8)
        if tag == 0:
            pass
        else:
            if (exist(id)):
                pass
            else:
                insert_tomato(id, tag, note, start, end)


def insert_tomato(id, tag, note, start, end):
    """
    番茄钟插入到notion
    """
    properties = Properties().title(note).select(
        "Category", dict[tag]).date("Date", start, end).number("Id", id)
    properties = notion_api.get_relation(properties)
    parent = DatabaseParent(TOMATO_DATABASE_ID)
    page = (
        Page()
        .parent(parent)
        .children(Children())
        .cover(unsplash.random())
        .icon("🍅")
        .properties(properties)
    )
    notion_api.create_page(page=page)


def exist(id):
    filter = {"property": "Id", "number": {"equals": id}}
    response = notion_api.query_database(TOMATO_DATABASE_ID, filter)
    results = response["results"]
    return len(results) > 0


def query_tomato():
    today = datetime.now().strftime("%Y-%m-%dT00:00:00+08:00")
    filter = {
        "and": [
            # {"property": "Date", "date": {"after": today}},
            {"property": "Toggl", "number": {"is_empty": True}}
        ]
    }
    sorts = [
        {
            "property": "Date",
            "direction": "ascending"
        }
    ]
    response = notion_api.query_database(TOMATO_DATABASE_ID,filter=filter,sorts= sorts)
    for result in response["results"]:
        page_id = id = result["id"]
        properties = result["properties"]
        category = properties["Category"]["select"]["name"]
        note = util.get_title(result,"Name")
        start = properties["Date"]["date"]["start"]
        duration = properties["Duration"]["formula"]["number"]
        id = insert_to_toggl(note,start,duration,dict2[category])
        update_tomato(page_id=page_id,id=id)

def update_tomato(page_id,id):
    properties = Properties().number("Toggl",id)
    notion_api.update_page(page_id=page_id,properties=properties)

def insert_to_toggl(description, start, duration, pid):
    auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")
    params = {
        "time_entry": {
            "description": description,
            "start": start,
            "duration": duration,
            "pid": pid,
            "created_with": "curl",
        }
    }
    response = requests.post(
        "https://api.track.toggl.com/api/v8/time_entries",
        json=params,
        auth=auth,
        headers=headers,
    )
    return response.json()["data"]["id"]


if __name__ == "__main__":
    user_id = login()
    get_plants(user_id)
    query_tomato()
