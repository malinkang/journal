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


def insert(content):
    content = json.loads(content)
    insert_to_notion(float(content["weight"]))

def insert_to_notion(weight):
    now = datetime.now()
    title = dateutils.format_date_with_week(date=now)
    cover = unsplash.random()
    properties = Properties().title(title).number("体重",weight)
    properties = notion.get_relation(properties,now,False)
    parent = DatebaseParent("8117b5547c7b44f5a3cb0fdfb2b464e4")
    page  = Page().parent(parent).children(Children()).cover(cover).icon("🏋️").properties(properties)
    notion_api.create_page(page=page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    insert(options.content)
