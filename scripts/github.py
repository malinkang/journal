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
tags: [{3}]
featured_image: "{4}"
categories: 2021
comment : false
---
'''
#获取内容
def getContent(secret,id,version):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers)
    return r
#获取星期
def getWeekDay():
    week_day_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    today = datetime.now().weekday()
    return week_day_dict[today]

#搜索需要同步的笔记
def search(secret,version,token):
    title = time.strftime("%m月%d日 星期"+getWeekDay(), time.localtime()) 
    headers = {'Authorization': secret,"Notion-Version":version}
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    result = r.json().get("results")[0]
    id = result.get("id")
    location = result.get("properties").get("位置").get("rich_text")[0].get("text").get("content")
    weather = result.get("properties").get("天气").get("rich_text")[0].get("text").get("content")
    external = result.get("cover").get("external")
    file = result.get("cover").get("file")
    if(not external is None):
        cover = external.get("url")
    elif(not file is None):
        cover = file.get("url")
    title =result.get("properties").get("标题").get("title")[0].get("text").get("content")
    createTime = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())
    week = datetime.now().strftime("%V")
    tag = "第"+week+"周"
    post = template.format(title,createTime,location+" "+weather,tag,cover)
    getPage(secret,id,version,token,post)
#创建post
def newPost(markdown,token):
    file = time.strftime('%Y-%m-%d', time.localtime())+".md"
    with open("./content/posts/"+file, "w") as f:
        f.seek(0)
        f.write(markdown)
        f.truncate()
    # body = {"message":"写日记","content":markdown}
    # file = time.strftime('%Y-%m-%d', time.localtime())+".md"
    # headers = {'Accept': 'application/vnd.github.v3+json',"Authorization":token}
    # r = requests.put('https://api.github.com/repos/malinkang/d/contents/content/posts/'+file,headers=headers,json=body)
    # print(r.text)

#解析文本
def parseText(text):
    r = ''
    for t in text:
        content = t.get("text").get("content")
        annotations =t.get("annotations")
        bold = annotations.get("bold")
        italic = annotations.get("italic")
        strikethrough = annotations.get("strikethrough")
        underline = annotations.get("underline")
        code = annotations.get("code")
        color = annotations.get("color")
        if(bold):
            content = "**"+content+"**"
        if(italic):
            content = "_"+content+"_"
        if(strikethrough):
           content = "~~"+content+"~~"
        if(underline):
            content = "<u>"+content+"</u>"
        if(code):
            content = "`"+content+"`"
        if(color !='default'):
            content = "<font color='"+color+"'>"+content+"</font>"
        r+=content
    return r
def getPage(secret,id,version,token,post):
    r = getContent(secret,id,version)
    results = r.json().get("results")
    for result in results:
        type = result.get("type")
        text = result.get(type).get("text")
        if(not text is None):
            #text是一个数组 如果text长度为0 说明是回车
            if(len(text)>0):
                content = parseText(text)
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
            external = result.get(type).get("external")
            file = result.get(type).get("file")
            if(not external is None):
                url = external.get("url")
            elif(not file is None):
                url = file.get("url")
            post += "![]("+url+")\n"
    print(post)
    post = base64.b64encode(post.encode(encoding='utf-8'))
    newPost(post.decode('ascii'),token)
    return r

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("token")
    options = parser.parse_args()
    search(options.secret,options.version,options.token)
