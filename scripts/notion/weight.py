#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json
import unsplash
import notion
import dateutils
from datetime import datetime, timedelta
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
from children import Children
import notion_api


def insert(content):
    content = json.loads(content)
    insert_to_notion(float(content["weight"]))

def insert_to_notion(weight):
    now = datetime.now() + timedelta(hours=8)
    title = dateutils.format_date_with_week(date=now)
    cover = unsplash.random()
    properties = Properties().title(title).date().number("体重",weight)
    properties = notion_api.get_relation(properties,now,False)
    parent = DatabaseParent("34c0db4313b24c3fac8e25436f5b3530")
    page  = Page().parent(parent).children(Children()).cover(cover).icon("🏋️").properties(properties)
    notion_api.create_page(page=page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    insert(options.content)
