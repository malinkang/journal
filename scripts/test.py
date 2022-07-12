import json
from multiprocessing import parent_process
import os
import pprint

# import feedparser
# import json
# # d = feedparser.parse("https://www.douban.com/feed/people/malinkang/interests")
# # for entry in d['entries']:
# #     print(json.dumps(entry))
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import argparse
import unsplash
import notion
import dateutils
from datetime import datetime, timedelta
from notion import Properties
from notion import Page
from notion_client import Client



# 创建Page
def create_page(pageId):
    emo = "☀️"
    tomorrow = datetime.now() + timedelta(days=1)
    week = tomorrow.strftime("第%V周")
    month = tomorrow.strftime("%-m月")
    title = dateutils.format_date_with_week(tomorrow)
    cover = unsplash.random()
    tags = [week,month]
    properties = Properties().title(title).date("日期",datetime.strftime(tomorrow, "%Y-%m-%d"),None).multi_select("标签",tags)
    properties = notion.get_relation(properties,tomorrow,False)
    page  = Page().parent(pageId).cover(cover).icon(emo).properties(properties)
    client = Client(auth="secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb")
    # page=json.dumps(page.parent)
    response=client.pages.create(parent=page.get_parent(),properties=page.get_properties())
    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id")
    options = parser.parse_args()
    # create_page(options.id)
    test = {'object': 'list', 'results': [{'object': 'page', 'id': 'bf7e75bb-9920-4fb5-a194-d0d4269a92c0', 'created_time': '2022-07-12T05:18:00.000Z', 'last_edited_time': '2022-07-12T05:18:00.000Z', 'created_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'last_edited_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '53514517-87d9-403f-b48d-9a9c20f31f43'}, 'archived': False, 'properties': {'date': {'id': '%3EORN'}, 'id': {'id': 'a%5D%3EN'}, 'url': {'id': 'eGey'}, 'image': {'id': 'f%3C%7CS'}, 'text': {'id': '~Yd%5D'}, 'Name': {'id': 'title'}}, 'url': 'https://www.notion.so/malinkang-bf7e75bb99204fb5a194d0d4269a92c0'}, {'object': 'page', 'id': 'fdbf8eae-911a-4fde-84e9-1bb2779074a9', 'created_time': '2022-07-12T04:13:00.000Z', 'last_edited_time': '2022-07-12T04:13:00.000Z', 'created_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'last_edited_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '53514517-87d9-403f-b48d-9a9c20f31f43'}, 'archived': False, 'properties': {'date': {'id': '%3EORN'}, 'id': {'id': 'a%5D%3EN'}, 'url': {'id': 'eGey'}, 'image': {'id': 'f%3C%7CS'}, 'text': {'id': '~Yd%5D'}, 'Name': {'id': 'title'}}, 'url': 'https://www.notion.so/malinkang-fdbf8eae911a4fde84e91bb2779074a9'}], 'next_cursor': None, 'has_more': False, 'type': 'page', 'page': {}}
    print(json.dumps(test))

