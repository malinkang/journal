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

template = '''
 {0}
今天是{1}年{2}，今天天气{3}，最高温度{4}，最低温度{5}，空气质量{6}。距离元旦还有{7}天。距离春节还有{8}天。睡眠时长{9}小时。体重{10}斤。

{11}
🏷  {12}

'''
#获取内容
def getContent(secret,id,version):
    headers = {'Authorization': secret,"Notion-Version":version}
    r = requests.get('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers)
    return r


#获取星期
#搜索需要同步的笔记
def search(secret,version,date):
    week_day_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    title = datetime.strftime(date,"%m月%d日 星期"+week_day_dict[date.weekday()])
    headers = {'Authorization': secret,"Notion-Version":version}
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    # print(r.text)
    result = r.json().get("results")[0]
    id = result.get("id")
    properties = result.get("properties")
    location = properties.get("位置").get("rich_text")[0].get("text").get("content")
    weather = properties.get("天气").get("rich_text")[0].get("text").get("content")
    highest = properties.get("最高温度").get("rich_text")[0].get("text").get("content")
    #
    highest = highest.replace("-","\\-")
    lowest = properties.get("最低温度").get("rich_text")[0].get("text").get("content")
    lowest = lowest.replace("-","\\-")
    aq = properties.get("空气质量").get("number")
    NewYear = properties.get("距离元旦").get("formula").get("number")
    SpringFestival = properties.get("距离春节").get("formula").get("number")
    
    if(properties.get("睡眠时长") is None):
        sleep = 0
    else:
        sleep = properties.get("睡眠时长").get("number")
    sleep = str(sleep).replace(".","\\.")
    if(properties.get("体重") is None):
        weight = 0
    else:
        weight = properties.get("体重").get("number")
    weight = str(weight).replace(".","\\.")
    print(sleep)
    #获取Tags
    tags = properties.get("标签").get("multi_select")
    tags = " ".join("\\#"+tag.get("name")for tag in tags)
    external = result.get("cover").get("external")
    file = result.get("cover").get("file")
    if(not external is None):
        cover = external.get("url")
    elif(not file is None):
        cover = file.get("url")
    emoji =result.get("icon").get("emoji")
    title = properties.get("标题").get("title")[0].get("text").get("content")
    year = datetime.now().year
    post = getPage(secret,id,version)
    message = template.format(emoji+title,year,title,weather,highest,lowest,aq,NewYear,SpringFestival,sleep,weight,post,tags)
    send(message,cover)

#创建markdown文件
def send(message,cover):
    url = "https://api.telegram.org/bot2055023678:AAETIYMOXp5Bj9X6T5-qx_0-hslX8FHi1Gc/sendPhoto"
    print(message)
    body = {
        "chat_id": "@pony2025",
        "photo": cover,
        "caption":message,
        "parse_mode": "MarkdownV2"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.request("POST", url, headers=headers, json=body)
    print(r.text)
   
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
        content = content.replace("~","\~")
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
def getPage(secret,id,version):
    post = ""
    r = getContent(secret,id,version)
    results = r.json().get("results")
    for result in results:
        type = result.get("type")
        text = result.get(type).get("text")
        if(not text is None):
            #text是一个数组 如果text长度为0 说明是回车
            if(len(text)>0):
                content = parseText(text)
                # 遇到标题前面多一个回车
                if(type=="heading_2"):
                    post +="\n*"+content+"*\n"
                elif(type=="to_do"):
                    post +="\- \[x\] "+content+"\n"
                elif(type=="bulleted_list_item"):
                    post +="· "+content+"\n"
                elif(type=="paragraph"):
                    post += content+"\n"
            else:
                post +="\n"
    return post


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("title")
    options = parser.parse_args()
    title = options.title
    if(len(title)==0):
        target = datetime.now()
    else:    
        target = datetime.strptime(title, '%Y%m%d')
    search(options.secret,options.version,target)
