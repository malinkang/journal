#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
from typing import ItemsView
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
categories: ["{5}"]
comment : false
---

今天是{6}年{7}，今天天气{8}，最高温度{9}，最低温度{10}，空气质量{11}。距离元旦还有{12}天。距离春节还有{13}天。睡眠时长{14}小时。体重{15}斤。

'''
#获取内容
def getContent(id):
    r = requests.get('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers)
    return r


def search():
    title = "Activity启动流程"
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    result = r.json().get("results")[0]
    id = result.get("id")
    properties = result.get("properties")
    getPage(id)

#创建markdown文件
def newPost(markdown,date):
    file = datetime.strftime(date,'%Y-%m-%d')+".md"
    with open("./content/posts/"+file, "w") as f:
        f.seek(0)
        f.write(markdown)
        f.truncate()

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

def getPage(id):
    post = ""
    r = getContent(id)
    print(r.text)
    results = r.json().get("results")
    for result in results:
        type = result.get("type")
        text = result.get(type).get("text")
        if(not text is None):
            #text是一个数组 如果text长度为0 说明是回车
            if(len(text)>0):
                content = parseText(text)
                if(type=="heading_2"):
                    post +="\n## "+content+"\n\n"
                elif(type=="to_do"):
                    post +="- [x] "+content+"\n"
                elif(type=="bulleted_list_item"):
                    post +="* "+content+"\n"
                elif(type=="numbered_list_item"):
                    post +="1. "+content+"\n"
                elif(type=="paragraph"):
                    post += content+"\n"
                elif(type=="code"):
                    language = result.get(type).get("language")
                    post += "```"+language+"\n"+content+"\n```\n"
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
    # newPost(header+post,date)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    options = parser.parse_args()
    headers = {'Authorization': options.secret,"Notion-Version":options.version}
    search()
