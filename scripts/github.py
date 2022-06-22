#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import requests
import argparse
import time
import dateutils

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


#获取星期
#搜索需要同步的笔记
def search(date):
    title = dateutils.format_date_with_week(date=date)
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    result = r.json().get("results")[0]
    print(result)
    id = result.get("id")
    properties = result.get("properties")
    if(properties.get("位置") is not None and len(properties.get("位置").get("rich_text"))>0):
        location = properties.get("位置").get("rich_text")[0].get("text").get("content")
    else:
        location = "未知"
    if(properties.get("天气") is not None and len(properties.get("天气").get("rich_text"))>0):
        weather = properties.get("天气").get("rich_text")[0].get("text").get("content")
    else:
        weather = "未知"
    if(properties.get("最高温度") is not None and len(properties.get("最高温度").get("rich_text"))>0):
        highest = properties.get("最高温度").get("rich_text")[0].get("text").get("content")
    else:
        highest = "未知"
    if(properties.get("最低温度") is not None and len(properties.get("最低温度").get("rich_text"))>0):
        lowest = properties.get("最低温度").get("rich_text")[0].get("text").get("content")
    else:
        lowest = "未知"
    if( properties.get("空气质量") is not None):
        aq = properties.get("空气质量").get("number")
    else:
        aq = 0
    NewYear = properties.get("距离元旦").get("formula").get("number")
    SpringFestival = properties.get("距离春节").get("formula").get("number")
    if(properties.get("睡眠时长") is not None):
        sleep = properties.get("睡眠时长").get("number")
    else:
        sleep = 0
    if(properties.get("体重") is not None):
        weight = properties.get("体重").get("number")
    else:
        weight = 0
    #获取Tags
    tags = properties.get("标签").get("multi_select")
    tags = ",".join("\""+tag.get("name")+"\""for tag in tags)
    external = result.get("cover").get("external")
    file = result.get("cover").get("file")
    if(external is not None):
        cover = external.get("url")
    elif(file is not None):
        cover = file.get("url")
    title =result.get("properties").get("标题").get("title")[0].get("text").get("content")
    createTime = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())
    year = datetime.now().year
    post = template.format(title,createTime,location+" "+weather,tags,cover,year,year,title,weather,highest,lowest,aq,NewYear,SpringFestival,sleep,weight)
    getPage(id,post,date)

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

def getPage(id,header,date):
    post = ""
    r = getContent(id)
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
    newPost(header+post,date)

headers ={}
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
    headers = {'Authorization': options.secret,"Notion-Version":options.version}
    search(target)
