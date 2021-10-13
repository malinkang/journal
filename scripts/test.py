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

from requests.api import get, post
def getChildrenBlock(secret,id,version):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers)
    return r
def parseText(text):
    print("-----")
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

def getPage(secret,id,version,location,weather):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/pages/'+id,headers=headers)
    content = r.json()
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
    post = template.format(title,createTime,location+" "+weather,tag,cover)
    r = getChildrenBlock(secret,id,version)
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
        # print(post)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("location")
    parser.add_argument("weather")
    options = parser.parse_args()
    getPage(options.secret, options.id,options.version,options.location,options.weather)