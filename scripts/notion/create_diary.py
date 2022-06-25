#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import unsplash
import notion
import dateutils
from datetime import datetime, timedelta
from properties import Properties
from page import Page
from datebase_parent import DatebaseParent
from children import Children
import notion_api


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
    parent = DatebaseParent(pageId)
    children = Children().add_block("bulleted_list_item","bulleted_list_item",color="red").add_block("to_do","todo1").add_block("heading_2","heading_2","https://developers.notion.com/reference/block")
    page  = Page().parent(parent).children(children).cover(cover).icon(emo).properties(properties)
    notion_api.create_page(page=page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("id")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    create_page(options.id)
