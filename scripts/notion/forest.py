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
FOREST_APP_VERSION = "4.53.0"
FOREST_LOGIN_URL = FOREST_URL_HEAD + "/api/v1/sessions"
FOREST_CLAENDAR_URL = (
    FOREST_URL_HEAD
    + "/api/v1/plants/updated_plants?update_since={date}&seekruid={user_id}"
)
FOREST_PLANTS_URL = FOREST_URL_HEAD + "/api/v1/products/coin_tree_types?seekrua=android_cn-" + \
    FOREST_APP_VERSION+"&seekruid={user_id}"
TODO = "97955f34653b4658bc0aaa50423be45f"
FOREST_TAG_URL = FOREST_URL_HEAD + "/api/v1/tags?seekruid={id}"
email = "linkang.ma@gmail.com"
password = "FFitness06"
headers = {"Content-Type": "application/json"}
s = requests.Session()
auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")

def login():
    data = {"session": {"email": email, "password": password}}
    r = s.post(FOREST_LOGIN_URL, headers=headers, json=data)
    user_id = r.json().get("user_id")
    return user_id


def get_user_profile(user_id):
    r = s.get(FOREST_TAG_URL.format(id=user_id), headers=headers)
    print(r.text)

def get_tags(user_id):
    dict = {}
    r = s.get(FOREST_TAG_URL.format(id=user_id), headers=headers)
    tags = r.json().get("tags")
    for tag in tags:
        id = tag.get("tag_id")
        name = tag.get("title")
        delete = tag.get("deleted")
        if not delete:
            dict[id] = name
    return dict
        

def get_plants_type(user_id):
    """
    获取所有的植物类型
    """
    r = s.get(FOREST_PLANTS_URL.format(user_id=user_id), headers=headers)
    print(r.text)
    # plants = r.json().get("coin_tree_types")
    # for plant in plants:
    #     id = plant.get("id")
    #     name = plant.get("name")
    #     print(id, name)


def get_plants(user_id):
    now = datetime.now().strftime("%Y-%m-%d")
    r = s.get(FOREST_CLAENDAR_URL.format(
        date=now, user_id=user_id), headers=headers)
    plants = r.json().get("plants")
    for plant in plants:
        id = plant.get("id")
        category = forest_tag_dict[plant.get("tag")]
        note = plant.get("note").strip()
        tags = []
        if note != "":
            tags = list(filter(lambda x:x.startswith("#"), note.split(" ")))
            tags = list(map(lambda x:x[1:], tags))
            note = list(filter(lambda x:not x.startswith("#"), note.split(" ")))[0]
        relation = get_relation(tags)
        start_time = plant.get("start_time")
        end_time = plant.get("end_time")
        start = date.format_utc(start_time) + timedelta(hours=8)
        end = date.format_utc(end_time) + timedelta(hours=8)
        if (exist(id)):
            pass
        else:
            insert_tomato(id,category, tags, note, start, end,relation)

def get_relation(tags):
    if(len(tags) > 0):
        filter = {"property": "Name", "rich_text": {"equals": tags[0]}}
        response = notion_api.query_database(database_id="e50dca03eafc47e7a4fda97191ee9426", filter=filter)
        return response.get("results")[0].get("id")
def insert_tomato(id, category,tags, note, start, end,relation):
    """
    番茄钟插入到notion
    """
    properties = Properties().title(note).select(
        "Category",category).multi_select("Tags",tags).date("Date", start, end).number("Id", id)
    properties = notion_api.get_relation(properties)
    if relation != None:
        properties.relation("Hour",relation)
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
    filter = {
        "and": [
            {"property": "Toggl", "number": {"is_empty": True}}
        ]
    }
    sorts = [
        {
            "property": "Date",
            "direction": "ascending"
        }
    ]
    response = notion_api.query_database(
        TOMATO_DATABASE_ID, filter=filter, sorts=sorts)
    print(response)
    for result in response["results"]:
        page_id= result["id"]
        properties = result["properties"]
        category = properties["Category"]["select"]["name"]
        tags = list(map(lambda x:x["name"], properties["Tags"]["multi_select"]))
        note = util.get_title(result, "Name")
        start = properties["Date"]["date"]["start"]
        duration = properties["Duration"]["formula"]["number"]
        id = insert_to_toggl(note, start, duration, toggl_project_dict[category],tags)
        update_tomato(page_id=page_id, id=id)


def update_tomato(page_id, id):
    properties = Properties().number("Toggl", id)
    notion_api.update_page(page_id=page_id, properties=properties)

def get_projects():
    dict = {}
    workspace_id = "5952284"
    url = f"https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/projects"
    response = requests.get(url, auth=auth, headers=headers)
    for project in response.json():
        id = project["id"]
        name = project["name"]
        dict[name] = id
    return dict

def insert_to_toggl(description, start, duration, pid,tags):
    print(tags)
    params = {
        "time_entry": {
            "description": description,
            "start": start,
            "duration": duration,
            "pid": pid,
            "created_with": "curl",
            "tags":tags
        }
    }
    response = requests.post(
        "https://api.track.toggl.com/api/v8/time_entries",
        json=params,
        auth=auth,
        headers=headers,
    )
    print(response.text)
    return response.json()["data"]["id"]


if __name__ == "__main__":
    user_id = login()
    forest_tag_dict = get_tags(user_id)
    get_plants(user_id)
    toggl_project_dict = get_projects()
    query_tomato()


