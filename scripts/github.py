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

from requests.api import get, post

template = '''---
title: "{0}"
date: {1}
description: "{2}"
tags: [{3},{4}]
featured_image: "{5}"
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
    
def getBlock(secret,pageId,version,token,location,content):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/blocks/'+pageId+'/children',headers=headers)
    newResults = filter(isToday,r.json().get("results"))
    for result in newResults:
         id = result.get("id")
         r = getPage(secret,id,version,token,location,content)
def isToday(result):
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime()) 
    print("isToday")
    print(result)
    return result.get("child_page")!=None and result.get("child_page").get("title")==title
def newPost(markdown,token):
    body = {"message":"写日记","content":markdown}
    file = time.strftime('%Y-%m-%d', time.localtime())+".md"
    headers = {'Accept': 'application/vnd.github.v3+json',"Authorization":token}
    requests.put('https://api.github.com/repos/malinkang/d/contents/content/posts/'+file,headers=headers,json=body)
def getYearProgress():
    from datetime import date, datetime
    complete ='▓'
    uncomplete ='░'
    print(complete)
    print(uncomplete)
    d0 = datetime(2021, 1, 1)
    d1 = datetime(2022, 1, 1)
    d3 = datetime.now()
    delta = d1 - d0
    delta2 = d3 - d0
    progress=(delta2.days+5)/delta.days
    print(round(progress*20))
    result = ""
    for i in range(0,round(progress*20)):
        result +=complete
    for i in range(0,20-round(progress*20)):
        result +=uncomplete
    result = "Year Progress "+result+" "+str(round(progress, 3)*100)+"%"
    return result
def getPage(secret,id,version,token,location,diary):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/pages/'+id,headers=headers)
    content = r.json()
    print(content)
    external = content.get("cover").get("external")
    file = content.get("cover").get("file")
    if(not external is None):
        cover = external.get("url")
    elif(not file is None):
        cover = file.get("url")
    title =content.get("properties").get("title").get("title")[0].get("text").get("content")
    createTime = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())
    week = datetime.now().strftime("%V")
    tag = "第"+week+"周"
    post = template.format(title,createTime,"",tag,location,cover)
    post += diary
    print(post)
    r = getChildrenBlock(secret,id,version)
    results = r.json().get("results")
    for result in results:
        type = result.get("type")
        text = result.get(type).get("text")
        if(not text is None):
            #text是一个数组 如果text长度为0 说明是回车
            if(len(text)>0):
                content = text[0].get("text").get("content")
                annotations = text[0].get("annotations")
                bold = annotations.get("bold")
                italic = annotations.get("italic")
                strikethrough = annotations.get("strikethrough")
                underline = annotations.get("underline")
                code = annotations.get("code")
                if(bold):
                    content = "**"+content+"**"
                if(italic):
                    content = "**"+content+"**"
                if(strikethrough):
                    content = "~~"+content+"~~"
                if(underline):
                    content = "<u>"+content+"</u>"
                if(code):
                    content = "`"+content+"`"
                if(type=="heading_2"):
                    post +="## "+content+"\n"
                elif(type=="to_do"):
                    post +="- [x] "+content+"\n"
                elif(type=="bulleted_list_item"):
                    post +="* "+content+"\n"
                elif(type=="paragraph"):
                    post += content+"\n"
            else:
                post +="\n"
        elif(type=="image"):
            url = result.get(type).get("external").get("url")
            post += "![]("+url+")\n"
    post = base64.b64encode(post.encode(encoding='utf-8'))
    newPost(post.decode('ascii'),token)
    return r
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("token")
    parser.add_argument("location")
    parser.add_argument("content")
    options = parser.parse_args()
    getBlock(options.secret, options.id,options.version,options.token,options.location,options.content)
