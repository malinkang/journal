#!/usr/bin/python
# -*- coding: UTF-8 -*-

# block对象：https://developers.notion.com/reference/block
from datetime import datetime
import json
import os
import unsplash
import requests


class Page(dict):
    def parent(self, database_id):
        dict = {}
        dict["database_id"] = database_id
        self["parent"] = dict
        return self
    def children(self, children):
        self["children"] = children
        return self
    def cover(self,cover):
        self["cover"] = {"type": "external", "external": {"url": cover}}
        return self
    def icon(self,icon):
        self["icon"] = {"type": "emoji", "emoji": icon}
        return self
    def properties(self,properties):
        self["properties"] = properties
        return self
    def get_parent(self):
        return json.dumps(self["parent"])
    def get_properties(self):
        return json.dumps(self["properties"])
class Properties(dict):
    """https://developers.notion.com/reference/property-value-object"""
    def title(self,title):
        self["title"] = {"title": [{"type": "text", "text": {"content": title}}]}
        return self
    def multi_select(self, property, list):
        multi_select = []
        for item in list:
            multi_select.append({"name": item})
        self[property] = {
            "type": "multi_select",
            "multi_select": multi_select,
        }
        return self
    def rich_text(self, property, text):
        rich_text = []
        rich_text.append({"type": "text", "text": {"content": text}})
        self[property] = {
            "rich_text": rich_text,
        }
        return self
    def select(self, property, name):
        self[property] = {"select": {"name": name}}
        return self
    def date(self, property, start,end):
        self[property] = {"date": {"start": start,"end":end}}
        return self
    def number(self,property,number):
        self[property] = {"number": number}
        return self


class Children(list):
    """"""

    def add_heading_2(self, content, link=None):
        self.add_rich_text("heading_2", content, link)
        return self

    def add_bulleted_list_item(self, content, link=None):
        self.add_rich_text("bulleted_list_item", content, link)
        return self

    def add_to_do(self, content, link=None):
        self.add_rich_text("to_do", content, link)
        return self

    """https://developers.notion.com/reference/rich-text"""

    def add_rich_text(self, type, content, link, color="default"):
        self.append(
            {
                "type": type,
                type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content,
                                "link": {"type": "url", "url": link},
                            },
                            "annotations": {
                                "color": color,
                            },
                        }
                    ]
                },
            }
        )
        return self


def get_heading_2(content):
    return {
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": content}}]},
    }


def get_paragraph(content):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"text": [{"type": "text", "text": {"content": content}}]},
    }


def get_bulleted_list_item(content):
    return {
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": content}}]
        },
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


def get_day_relation(year_id, date):
    day = datetime.strftime(date, "%m月%d日 星期" + week_day_dict[date.weekday()])
    body = {
        "filter": {
            "and": [
                {"property": "标题", "text": {"equals": day}},
                {
                    "property": "年",
                    "relation": {"contains": get_year_releation(year_id)},
                },
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/294060cde13e4c29b0ac6ee490c8a448/query",
        headers=headers,
        json=body,
    )
    
    return r.json().get("results")[0].get("id")


def search(id, title):
    body = {"filter": {"and": [{"property": "Name", "text": {"equals": title}}]}}
    r = requests.post(
        "https://api.notion.com/v1/databases/" + id + "/query",
        headers=headers,
        json=body,
    )
    # print(r.text)
    results = r.json().get("results")
    if len(results) == 0:
        return None
    return results[0].get("id")


WEEK_PAGE_ID = "194f66886cd8479899d38b0fb0b7da26"


def get_week_relation(year_id, date):
    year = date.isocalendar().year
    week = date.isocalendar().week
    week = "第" + str(week) + "周"
    week_json_file = DATA_DIR + str(year) + "/" + week + ".json"
    if os.path.exists(week_json_file):
        with open(week_json_file, "r") as json_file:
            return json.load(json_file).get("id")

    body = {
        "filter": {
            "and": [
                {"property": "Name", "text": {"equals": week}},
                {"property": "年", "relation": {"contains": year_id}},
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/" + WEEK_PAGE_ID + "/query",
        headers=headers,
        json=body,
    )
    if len(r.json().get("results")) == 0:
        return None
    else:
        id = r.json().get("results")[0].get("id")
    json_data = {"id": id}
    with open(week_json_file, "w") as outfile:
        json.dump(json_data, outfile)
    return id


def get_month_relation(year_id, year, month):
    id = ""
    month_json_file = DATA_DIR + year + "/" + month + ".json"
    if os.path.exists(month_json_file):
        with open(month_json_file, "r") as json_file:
            return json.load(json_file).get("id")
    body = {
        "filter": {
            "and": [
                {"property": "Name", "text": {"equals": month}},
                {"property": "年", "relation": {"contains": year_id}},
            ]
        }
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/dd39319e45964a64899ae5371c0a6421/query",
        headers=headers,
        json=body,
    )
    if len(r.json().get("results")) == 0:
        return None
    else:
        id = r.json().get("results")[0].get("id")
    json_data = {"id": id}
    with open(month_json_file, "w") as outfile:
        json.dump(json_data, outfile)
    return id


DATA_DIR = "./data/"


def get_year_releation(year):
    id = ""
    year_json_file = DATA_DIR + year + "/id.json"
    if os.path.exists(year_json_file):
        with open(year_json_file, "r") as json_file:
            return json.load(json_file).get("id")
    body = {"filter": {"and": [{"property": "Name", "text": {"equals": year}}]}}
    r = requests.post(
        "https://api.notion.com/v1/databases/f4d2374344ca409aa22d40e8d33833eb/query",
        headers=headers,
        json=body,
    )
    # 如果返回结果为空，则创建年份
    if len(r.json().get("results")) == 0:
        # TODO
        return None
    else:
        id = r.json().get("results")[0].get("id")
    json_data = {"id": id}
    year_dir = "./data/" + year
    if os.path.exists(year_dir) == False:
        os.makedirs(year_dir)
    with open(year_json_file, "w") as outfile:
        json.dump(json_data, outfile)
    return id


def get_relation(properties, date=datetime.now(), include_day=False):
    year = date.strftime("%Y")
    month = date.strftime("%-m月")

    year_id = get_year_releation(year)
    properties["年"] = {
        "relation": [
            {
                "id": year_id,
            }
        ]
    }
    properties["月"] = {
        "relation": [
            {
                "id": get_month_relation(year_id, year, month),
            }
        ]
    }
    properties["周"] = {
        "relation": [
            {
                "id": get_week_relation(year_id, date),
            }
        ]
    }
    if include_day:
        properties["日"] = {
            "relation": [
                {
                    "id": get_day_relation(year_id, date),
                }
            ]
        }
    return properties
