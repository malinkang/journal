#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import argparse
import dateutils
from filter import Filter
import notion_api
from page import Page
from properties import Properties


#搜索笔记
def search(content):
    title = dateutils.format_date_with_week()
    filter = {"property":"Name","rich_text":{"equals":title}}
    response = notion_api.query_database("294060cd-e13e-4c29-b0ac-6ee490c8a448",filter)
    if(len([response["results"]])>0):
        id = response["results"][0].get("id")
        update(id,content)
    

def emoji(weather):
    if("晴" in weather):
        return "☀️"
    elif("雨" in weather):
        return "🌧"
    elif("雪" in weather):
        return "❄️"
    elif("云" in weather):
        return "☁️"
    elif("雾" in weather):
        return "🌫"
    else:
        return "☀️"


def update(id, content):
    content = json.loads(content)
    weather = content['weather']
    highest = content['highest']
    lowest = content['lowest']
    aqi = content['aqi']
    emo = emoji(weather)
    properties=Properties().rich_text("天气",weather).rich_text("最高温度",highest).rich_text("最低温度",lowest).number("空气质量",int(aqi))
    page = Page().icon(emo).properties(properties)
    notion_api.update_page(id,page)
    
                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    search(options.content)
