#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, datetime, timedelta, timezone
import requests
import argparse
import time
import notion

from datetime import datetime
import dateutils
from filter import Filter

from requests.api import get
import notion_api


def getWeekDay():
    week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
    today = datetime.now().weekday()
    return week_day_dict[today]


def createDiary(title, startTime, endTime):
    body = {
        "parent": {
            "type": "database_id",
            "database_id": "101341b8f9634e7a9ad522103db35731",
        },
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]},
            "时间": {"date": {"start": startTime, "end": endTime}},
        },
        "icon": {"type": "emoji", "emoji": "😄"},
    }
    r = requests.post("https://api.notion.com/v1/pages/", headers=headers, json=body)
    print(r.text)


def get_time():
    now = datetime.now()
    # 时区问题 所以要减去8小时
    now = datetime(now.year, now.month, now.day - 1, 15, 30).astimezone(
        tz=timezone(timedelta(hours=8))
    )
    date = now.replace(microsecond=0).isoformat()
    body = {
        "filter": {"or": [{"timestamp": "created_time", "created_time": {"after": date}}]},
        "sorts": [{"timestamp": "created_time", "direction": "ascending"}],
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/5351451787d9403fb48d9a9c20f31f43/query",
        headers=headers,
        json=body,
    )
    children = []
    results = r.json().get("results")
    if (results is not None and len(results) > 0):
        children.append(notion.get_divider())
        children.append(notion.get_heading_2("💬 碎碎念"))
        for result in results:
            properties = result.get("properties")
            content = properties.get("text").get("rich_text")[0].get("text").get("content")
            children.append(notion.get_bulleted_list_item(content))
    body = {
        "filter": {"or": [{"property": "时间", "date": {"after": date}}]},
        "sorts": [{"property": "时间", "direction": "ascending"}],
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/d8eee75d8c1049e7aa3dd6614907bb04/query",
        headers=headers,
        json=body,
    )
    results = r.json().get("results")
    if (results is not None and len(results) > 0):
        children.append(notion.get_divider())
        children.append(notion.get_heading_2("📅 今日日程"))
        for result in results:
            properties = result.get("properties")
            name = properties.get("二级分类").get("select").get("name")
            if (properties.get("备注") is not None and len(properties.get("备注").get("rich_text")) > 0):
                name += "，"+properties.get("备注").get("rich_text")[0].get("text").get("content")
            
            startTime = properties.get("时间").get("date").get("start")
            endTime = properties.get("时间").get("date").get("end")

            start = datetime.strftime(
                datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S.000+08:00"), "%H:%M"
            )
            end = datetime.strftime(
                datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S.000+08:00"), "%H:%M"
            )
            content = start + "~" + end + " " + name
            children.append(notion.get_bulleted_list_item(content))
    search(children)




def getBlock(id, children):
    r = requests.get("https://api.notion.com/v1/blocks/" + id, headers=headers)
    append(r.json().get("id"), children)


# 添加block
def append(id, children):
    body = {"children": children}
    r = requests.patch(
        "https://api.notion.com/v1/blocks/" + id + "/children",
        headers=headers,
        json=body,
    )
    # print(r.text)


# 搜索需要同步的笔记
def search(children):
    print(children)
    title = dateutils.format_date_with_week()
    filter = Filter("标题","rich_text","equals",title)
    response = notion_api.query_database("294060cd-e13e-4c29-b0ac-6ee490c8a448",filter)
    if(len([response["results"]])>0):
        id = response["results"][0].get("id")
        append(id, children)


headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    options = parser.parse_args()
    headers = {"Authorization": options.secret, "Notion-Version": options.version}
    get_time()
