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


def get_plants(user_id):
    """tag:15 工作"""
    now = datetime.now().strftime("%Y-%m-%d")
    r = s.get(FOREST_CLAENDAR_URL.format(date=now, user_id=user_id), headers=headers)
    results = []
    for plant in r.json().get("plants"):
        id = plant.get("id")
        note = plant.get("note").strip()
        start_time = plant.get("start_time")
        end_time = plant.get("end_time")
        start = date.format_utc(start_time) + timedelta(hours=8)
        end = date.format_utc(end_time) + timedelta(hours=8)
        if note == "":
            pass
        else:
            if(exist(id)):
                pass
            else:
                insert_tomato(id,note, start, end)



def search_todo(title):
    filter = {"property": "Title", "rich_text": {"equals": title}}
    response = notion_api.query_database(TODO, filter)
    if len(response.get("results")) == 0:
        return None
    return response.get("results")[0]


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
    response = notion_api.create_page(page=page)
    return response


# 番茄钟插入notion
def insert_tomato(id,note, start, end):
    result = search_todo(note)
    properties = Properties().title(note).date("Date", start, end).number("Id",id)
    properties = notion_api.get_relation(properties)
    if(result!=None):
        properties["ToDo"] = {"relation": [{"id": result["id"]}]}
    parent = DatabaseParent(TOMATO)
    page = (
        Page()
        .parent(parent)
        .children(Children())
        .cover(unsplash.random())
        .icon("🍅")
        .properties(properties)
    )
    notion_api.create_page(page=page)
    return result

def exist(id):
    filter = {"property": "Id", "number": {"equals": id}}
    response=notion_api.query_database(TOMATO, filter)
    results = response["results"]
    return len(results)>0



# 插入Toggl
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
    print(response.text)


if __name__ == "__main__":
    login()
