#!/usr/bin/python
# -*- coding: UTF-8 -*-
from calendar import week
from datetime import datetime, timedelta
import argparse
import unsplash

from datetime import datetime
import notion_api
from notion_api import Properties
from notion_api import Page
from notion_api import Children
from notion_api import DatabaseParent

# 1.获取正在读的书籍


def get_reading(end):
    filter = {"property": "状态", "select": {"equals": "在读"}}
    response = notion_api.query_database("c7efdba75f4146ad84a3f5b773998859", filter)
    if len(response.get("results")) > 0:
        name = notion_api.get_title(response, "标题")
        id = response.get("results")[0].get("id")
        start = get_yestorday(id)
        add(name, id, start, end)


def add(title, id, start, end):
    properties = (
        Properties()
        .title(title)
        .relation("Book", id)
        .number("Start", int(start))
        .number("End", int(end))
        .date()
    )
    properties = notion_api.get_relation(properties)
    page = (
        Page()
        .parent(DatabaseParent("cca71ece15ac48a68c34e5f86a2e6b38"))
        .children(Children())
        .properties(properties)
        .cover(unsplash.random())
        .icon("📚")
    )
    notion_api.create_page(page)


# 获取昨天的数据
def get_yestorday(id):
    filter = {"property": "Book", "relation": {"contains": id}}
    sorts = [{"property": "Date", "direction": "descending"}]
    response = notion_api.query_database(
        "cca71ece15ac48a68c34e5f86a2e6b38", filter, sorts
    )
    page = 0
    if len(response.get("results")) > 0:
        page = notion_api.get_number(response, "End")
    return page


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("end")
    options = parser.parse_args()
    get_reading(options.end)
