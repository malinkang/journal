#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json
import unsplash
import notion
import dateutils
from datetime import datetime, timedelta
from properties import Properties
from page import Page
from datebase_parent import DatebaseParent
from children import Children
import notion_api
import requests



# 搜索笔记
def search(content):
    content = json.loads(content)
    weight = content["weight"]
    insert_to_notion(weight)


def insert_to_notion(weight):
    now = datetime.now()
    title = dateutils.format_date_with_week(date=now)
    cover = unsplash.random()
    properties = Properties().title(title).number("体重",weight)
    properties = notion.get_relation(properties,now,False)
    parent = DatebaseParent("34c0db4313b24c3fac8e25436f5b3530")
    page  = Page().parent(parent).children(Children()).cover(cover).icon("").properties(properties)
    notion_api.create_page(page=page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    search(options.content)
