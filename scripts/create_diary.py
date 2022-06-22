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




# 创建Page
def create_page(pageId):
    emo = "☀️"
    tomorrow = datetime.now() + timedelta(days=1)
    week = tomorrow.strftime("第%V周")
    month = tomorrow.strftime("%-m月")
    title = dateutils.format_date_with_week(date=tomorrow)
    cover = unsplash.random()
    tags = [week,month]
    properties = Properties().title(title).date("日期",datetime.strftime(tomorrow, "%Y-%m-%d"),None).multi_select("标签",tags)
    properties = notion.get_relation(properties,tomorrow,False)
    page  = Page().parent(pageId).cover(cover).icon(emo).properties(properties)
    print(title)
    r= requests.post("https://api.notion.com/v1/pages/", headers=headers, json=page)
    print(r.text)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    headers = {"Authorization": options.secret, "Notion-Version": options.version}
    create_page(options.id)
