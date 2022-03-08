#!/usr/bin/python
# -*- coding: UTF-8 -*-

# block对象：https://developers.notion.com/reference/block
from calendar import month, week
from datetime import datetime
from webbrowser import get
import unsplash
import requests


def get_heading_2(content):
    return {
        "type": "heading_2",
        "heading_2": {"text": [{"type": "text", "text": {"content": content}}]},
    }


def get_paragraph(content):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"text": [{"type": "text", "text": {"content": content}}]},
    }


def get_todo(content, url=None):
    text = {}
    if content is not None:
        text["content"] = content
    if url is not None:
        text["link"] = {"url": url}
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "text": [
                {
                    "type": "text",
                    "text": text,
                }
            ],
            "checked": False,
        },
    }


def get_image(url):
    return {
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": url},
        },
    }


def get_divider():
    return {
        "type": "divider",
        "divider": {},
    }


def get_title(title):
    return {"title": [{"type": "text", "text": {"content": title}}]}


def get_cover():
    return {"type": "external", "external": {"url": unsplash.random()}}


headers = {
    "Authorization": "Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb",
    "Notion-Version": "2021-08-16",
}


week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}


def get_day_relation(date):
    year = date.strftime("%Y")
    day = datetime.strftime(date, "%m月%d日 星期" + week_day_dict[date.weekday()])
    body = {
        "filter": {
            "and": [
                {"property": "标题", "text": {"equals": day}},
                {"property": "年", "relation": {"contains": get_year_releation(year)}},
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/294060cde13e4c29b0ac6ee490c8a448/query",
        headers=headers,
        json=body,
    )
    # print(day)
    # print(r.text)
    return r.json().get("results")[0].get("id")


def search(id,title):
    body = {
        "filter": {
            "and": [
                {"property": "Name", "text": {"equals": title}}
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/"+id+"/query",
        headers=headers,
        json=body,
    )
    # print(r.text)
    return r.json().get("results")[0].get("id")



def get_week_relation(year,week):
    print(week)
    body = {
        "filter": {
            "and": [
                {"property": "Name", "text": {"equals": week}},
                {"property": "年", "relation": {"contains": year}},
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/194f66886cd8479899d38b0fb0b7da26/query",
        headers=headers,
        json=body,
    )
    # print(r.text)
    return r.json().get("results")[0].get("id")

def get_month_relation(year,month):
    print(month)
    body = {
        "filter": {
            "and": [
                {"property": "Name", "text": {"equals": month}},
                {"property": "年", "relation": {"contains": year}},
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/dd39319e45964a64899ae5371c0a6421/query",
        headers=headers,
        json=body,
    )
    return r.json().get("results")[0].get("id")


def get_year_releation(year):
    body = {"filter": {"and": [{"property": "Name", "text": {"equals": year}}]}}
    r = requests.post(
        "https://api.notion.com/v1/databases/f4d2374344ca409aa22d40e8d33833eb/query",
        headers=headers,
        json=body,
    )
    return r.json().get("results")[0].get("id")


def get_relation(properties, date=datetime.now(),include_day = True):
    year = date.strftime("%Y")
    month = date.strftime("%-m月")
    week = "第" + date.strftime("%-V") + "周"
    
    year = get_year_releation(year)
    properties["年"] = {
        "relation": [
            {
                "id": year,
            }
        ]
    }
    properties["月"] = {
        "relation": [
            {
                "id": get_month_relation(year,month),
            }
        ]
    }
    properties["周"] = {
        "relation": [
            {
                "id": get_week_relation(year,week),
            }
        ]
    }
    if include_day:
        properties["日"] = {
            "relation": [
                {
                    "id": get_day_relation(date),
                }
            ]
        }
    return properties
