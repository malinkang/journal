#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import argparse
from requests.api import get
import dateutils



#搜索笔记
def search(secret,version,content):
    title = dateutils.format_date_with_week()
    headers = {'Authorization': secret,"Notion-Version":version}
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    result = r.json().get("results")[0]
    id = result.get("id")
    update(secret,version,id,content)
    

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


def update(secret, version,pageId, content):
    content = json.loads(content)
    weather = content['weather']
    highest = content['highest']
    lowest = content['lowest']
    aqi = content['aqi']
    emo = emoji(weather)
    headers = {'Authorization': secret, "Notion-Version": version}
    body = {
        "properties": {
       "天气": {"rich_text": [{"type": "text", "text": {"content": weather}}]},
       "最高温度": {"rich_text": [{"type": "text", "text": {"content": highest}}]},
       "最低温度": {"rich_text": [{"type": "text", "text": {"content": lowest}}]},
       "空气质量": {"number": int(aqi)},
    },
        "icon": {"type": "emoji", "emoji": emo}
    }
    r = requests.patch('https://api.notion.com/v1/pages/'+pageId,
                      headers=headers, json=body)
    print(r.text)
                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("content")
    options = parser.parse_args()
    search(options.secret, options.version,options.content)
