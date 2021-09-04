#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import os
import base64
import argparse
import time
import sys

from datetime import datetime

from requests.api import get, post

template = '''---
title: "{0}"
date: {1}
description: ""
tags: [{2}]
featured_image: "{3}"
categories: 2021
comment : false
---
'''

def getChildrenBlock(secret,id,version):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers)
    return r

def getWeekDay():
    week_day_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    today = datetime.now().weekday()
    return week_day_dict[today]
    
def getBlock(secret,pageId,version,token):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/blocks/'+pageId+'/children',headers=headers)
    newResults = filter(isToday,r.json().get("results"))
    for result in newResults:
         id = result.get("id")
         r = getPage(secret,id,version,token)
def isToday(result):
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime()) 
    return result.get("child_page").get("title")==title
def newPost(markdown,token):
    body = {"message":"写日记","content":markdown}
    file = time.strftime('%Y-%m-%d', time.localtime())+".md"
    headers = {'Accept': 'application/vnd.github.v3+json',"Authorization":token}
    r = requests.put('https://api.github.com/repos/malinkang/diary/contents/2021/'+file,headers=headers,json=body)
    print(r.json())
    return r
def getPage(secret,id,version,token):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/pages/'+id,headers=headers)
    content = r.json()
    cover = content.get("cover").get("external").get("url")
    title =content.get("properties").get("title").get("title")[0].get("text").get("content")
    createTime = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())
    week = datetime.now().strftime("%V")
    tag = "第"+week+"周"
    post = template.format(title,createTime,tag,cover)
    print(post)
    r = getChildrenBlock(secret,id,version)
    results = r.json().get("results")
    for result in results:
            type = result.get("type")
            text = result.get(type).get("text")
            if(len(text)>0):
                content = text[0].get("text").get("content")
                if(type=="heading_2"):
                    post +="## "+content+"\n"
                elif(type=="to_do"):
                    post +="- [x] "+content+"\n"
    print(post)
    post = base64.b64encode(post.encode(encoding='utf-8'))
    newPost(post.decode('ascii'),token)
    return r
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("token")
    options = parser.parse_args()
    getBlock(options.secret, options.id,options.version,options.token)