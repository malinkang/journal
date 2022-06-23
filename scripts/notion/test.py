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
    create_page(options.id)
