#!/usr/bin/python
# -*- coding: UTF-8 -*-
from calendar import week
from datetime import date, datetime, timedelta
import argparse
from pydoc import pager
import unsplash

from datetime import datetime
import notion_api
from notion_api import Properties
from notion_api import Page
from notion_api import Children
from notion_api import DatabaseParent

DATABASE_ID = 'cca71ece15ac48a68c34e5f86a2e6b38'

# 1.获取正在读的书籍
def get_reading(end):
    filter = {"property": "状态", "select": {"equals": "在读"}}
    response = notion_api.query_database("c7efdba75f4146ad84a3f5b773998859", filter)
    if len(response.get("results")) > 0:
        name = notion_api.get_title(response, "标题")
        id = response.get("results")[0].get("id")
        get_today(name,id,end)
        # 


def insert(title, id, start, end):
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



def get_today(name,id,end):
    today = datetime.now().strftime("%Y-%m-%d")
    filter = {'and':[
        {"property": "Date", "date": {"equals": today}},
        {"property": "Book", "relation": {"contains": id}}
    ]}
    response = notion_api.query_database(database_id=DATABASE_ID,filter=filter)
    if len(response.get("results")) > 0:
        page = notion_api.get_number(response, "End")
        id = response.get('results')[0].get('id')
        update_today(id,end)
    else:
        start = get_lastest(id)
        insert(name, id, start, end)

def update_today(id,end):
    properties = (
        Properties()
        .number('End',int(end))
    )
    notion_api.update_page(page_id=id,properties=properties)
# 获取最新的数据
def get_lastest(id):
    filter = {"property": "Book", "relation": {"contains": id}}
    sorts = [{"property": "Date", "direction": "descending"}]
    response = notion_api.query_database(
        DATABASE_ID, filter, sorts
    )
    page = 1
    if len(response.get("results")) > 0:
        page = notion_api.get_number(response, "End")
    return page


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("end")
    options = parser.parse_args()
    get_reading(options.end)
