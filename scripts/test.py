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
    # options = parser.parse_args()
    # create_page(options.id)
    test = {'parent': {'type': 'database_id', 'database_id': '48107861338540dc97f6985be1e2a198'}, 'properties': {'title': {'title': [{'type': 'text', 'text': {'content': '07月12日 星期二'}}]}, 'slug': {'rich_text': [{'type': 'text', 'text': {'content': '2022-07-12'}}]}, 'status': {'select': {'name': 'Published'}}, 'type': {'select': {'name': 'Post'}}, 'date': {'date': {'start': '2022-07-12T14:55:19.700502', 'end': None, 'time_zone': 'Asia/Shanghai'}}, 'tags': {'type': 'multi_select', 'multi_select': [{'name': '第28周'}, {'name': '7月'}]}}, 'children': [{'object': 'block', 'type': 'paragraph', 'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': ''}}], 'color': 'default'}}, {'object': 'block', 'type': 'heading_2', 'heading_2': {'rich_text': [{'type': 'text', 'text': {'content': '📅 倒数日'}}], 'color': 'default'}}, {'object': 'block', 'type': 'bulleted_list_item', 'bulleted_list_item': {'rich_text': [{'type': 'text', 'text': {'content': '今年还有172 天 ■■■■■□□□□□ 52%'}}], 'color': 'default'}}, {'object': 'block', 'type': 'heading_2', 'heading_2': {'rich_text': [{'type': 'text', 'text': {'content': '✅ ToDo'}}], 'color': 'default'}}, {'object': 'block', 'type': 'to_do', 'to_do': {'rich_text': [{'type': 'text', 'text': {'content': '读《鼠疫La Peste》441-480》鼠疫La Peste'}}], 'color': 'default'}, 'checked': True}, {'object': 'block', 'type': 'heading_2', 'heading_2': {'rich_text': [{'type': 'text', 'text': {'content': '❤️ 健康'}}], 'color': 'default'}}, {'object': 'block', 'type': 'bulleted_list_item', 'bulleted_list_item': {'rich_text': [{'type': 'text', 'text': {'content': '体重：20斤'}}], 'color': 'default'}}, {'object': 'block', 'type': 'heading_2', 'heading_2': {'rich_text': [{'type': 'text', 'text': {'content': '💬 碎碎念'}}], 'color': 'default'}}, {'object': 'block', 'type': 'embed', 'embed': {'url': 'https://twitter.com/malinkang/status/1546723763504685056'}}, {'object': 'block', 'type': 'embed', 'embed': {'url': 'https://twitter.com/malinkang/status/1546693663165763586'}}], 'icon': {'type': 'emoji', 'emoji': '☀️'}, 'cover': {'type': 'external', 'external': {'url': 'https://images.unsplash.com/photo-1655161916155-38696d96bab8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=Mnw2ODUwfDB8MXxyYW5kb218fHx8fHx8fHwxNjU3NTkzMTMx&ixlib=rb-1.2.1&q=80&w=400'}}}
    print(json.dumps(test))
