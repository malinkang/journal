# -*- coding: utf-8 -*-
#!/usr/bin/python

from datetime import datetime, timedelta
import json
import unsplash
import requests
import notion
import date
from notion_api import Properties
from notion_api import Page
import notion_api
from notion_api import DatabaseParent
from notion_api import Children

FOREST_URL_HEAD = "https://forest-china.upwardsware.com"
FOREST_LOGIN_URL = FOREST_URL_HEAD + "/api/v1/sessions"
FOREST_CLAENDAR_URL = (
    FOREST_URL_HEAD
    + "/api/v1/plants/updated_plants?update_since={date}&seekruid={user_id}"
)
TODO = "97955f34653b4658bc0aaa50423be45f"
TOMATO = "bcdcfb9068eb458a94c8266c2b88ec09"
FOREST_TAG_URL = FOREST_URL_HEAD + "/api/v1/tags?seekruid={id}"
email = "linkang.ma@gmail.com"
password = "FFitness06"
headers = {"Content-Type": "application/json"}
USER_ID = "6d411501-82d6-46e5-b809-97c0fdce722c"
s = requests.Session()


def login():
    data = {"session": {"email": email, "password": password}}
    r = s.post(FOREST_LOGIN_URL, headers=headers, json=data)
    user_id = r.json().get("user_id")
    get_plants(user_id)


# 获取植物
def get_plants(user_id):
    now = datetime.now().strftime("%Y-%m-%d")
    r = s.get(FOREST_CLAENDAR_URL.format(date=now, user_id=user_id), headers=headers)
    for plant in r.json().get("plants"):
        note = plant.get("note")
        start_time = plant.get("start_time")
        end_time = plant.get("end_time")
        start = date.format_utc(start_time) + timedelta(hours=8)
        end = date.format_utc(end_time) + timedelta(hours=8)
        if note == "":
            pass
        else:
            insert_tomato(note, start, end)
    update_todo()


def search_todo(title):
    id = notion.search(TODO, title)
    if id is None:
        return insert_todo(title)
    return id


def insert_todo(title):
    properties = (
        Properties()
        .title(title)
        .select("Status", "Completed")
        .select("Priority", "High 🔥")
        .people("Assign", ["6d411501-82d6-46e5-b809-97c0fdce722c"])
    )
    parent = DatabaseParent(TODO)
    page = (
        Page()
        .parent(parent)
        .children(Children())
        .cover(unsplash.random())
        .icon("✅")
        .properties(properties)
    )
    print("test == " + json.dumps(page))
    response = notion_api.create_page(page=page)
    return response.get("id")


# 番茄钟插入notion
def insert_tomato(note, start, end):
    print(start)
    properties = Properties().title(note).date("Date", start, end)
    properties = notion_api.get_relation(properties)
    properties["ToDo"] = {"relation": [{"id": search_todo(note)}]}
    parent = DatabaseParent(TOMATO)
    page = (
        Page()
        .parent(parent)
        .children(Children())
        .cover(unsplash.random())
        .icon("🍅")
        .properties(properties)
    )
    response = notion_api.create_page(page=page)
    return response.get("id")


def get_end_time(title):
    filter = {"property": "Name", "rich_text": {"equals": title}}
    sorts = [{"property": "Date", "direction": "ascending"}]
    response = notion_api.query_database(TOMATO, filter, sorts)
    results = response.get("results")
    size = len(results)
    start = notion_api.get_date(response).get("start")
    end = notion_api.get_date(response, index=size - 1).get("end")
    return (start, end)


# 更新todo的时间
def update_todo():
    filter = {
        "and": [
            {"property": "Date", "date": {"is_empty": True}},
            {"property": "🍅", "rollup": {"number": {"greater_than": 0}}},
        ]
    }
    response = notion_api.query_database(TODO, filter)
    for index in range(0, len(response.get("results"))):
        print("index" + str(index))
        page_id = response.get("results")[index].get("id")
        print(page_id)
        title = notion_api.get_title(response, "Name", index=index)
        ret = get_end_time(title)
        properties = Properties().date(start=ret[0], end=ret[1], time_zone=None)
        response2 = notion_api.update_page(page_id, properties)
        duration = notion_api.get_formula(response2, "Duration", type="number")
        insert_to_toggl(title, ret[0], duration, "177393358")


# 插入Toggle
def insert_to_toggl(description, start, duration, pid):
    print("insert_to_toggl")
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
    print(response.text)


if __name__ == "__main__":
    login()
    # update_todo()
    # get_end_time("hugo自动化脚本编写")
