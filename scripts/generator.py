#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import os
import base64
import argparse
import time
from datetime import datetime

from requests.api import get

def getWeekDay():
    week_day_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    today = datetime.now().weekday()
    return week_day_dict[today]

def createDiary(secret,pageId,version):
    headers = {'Authorization': secret,"Notion-Version":version}
    cover = "https://images.unsplash.com/photo-1529963183134-61a90db47eaf?ixid=MnwxMjA3fDB8MHx0b3BpYy1mZWVkfDMwfDZzTVZqVExTa2VRfHxlbnwwfHx8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60"
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime()) 
    body = {"parent":{"type":"page_id","page_id":pageId},"properties":{"title":{"title":[{"type":"text","text":{"content":title}}]}},"cover":{"type":"external","external":{"url":cover}},"icon":{"type":"emoji","emoji":"🌚"},"children":[{"type":"heading_2","heading_2":{"text":[{"type":"text","text":{"content":"工作"}}]}},{"type":"heading_2","heading_2":{"text":[{"type":"text","text":{"content":"学习"}}]}},{"object":"block","type":"to_do","to_do":{"text":[{"type":"text","text":{"content":"跑步5km🍅"}}],"checked":False}}]}
    r = requests.post('https://api.notion.com/v1/pages/',headers=headers,json=body)
    print(r.text)
    

# print(datetime(2021,8,29).strftime('%W'))
# print(week)
# r = getNotionPage(root_page_id)

# r = getChildrenBlock(r.json().get("id"))
# print(r.text)
# # r = createPage()
# print(r.text)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    options = parser.parse_args()
    createDiary(options.secret, options.id,options.version)