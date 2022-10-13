#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import requests
import argparse

from requests.api import get, post


map = {
    1:"1️⃣",
    2:"2️⃣",
    3:"3️⃣",
    4:"4️⃣",
    5:"5️⃣",
    6:"6️⃣",
    7:"7️⃣",
    8:"8️⃣",
    9:"9️⃣",
    10:"🔟",
}
#获取星期
#搜索需要同步的笔记
def search(date):
    week_day_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
    title = datetime.strftime(date,"%m月%d日 星期"+week_day_dict[date.weekday()])
    body={"query":title}
    r = requests.post("https://api.notion.com/v1/search",headers=headers,json=body)
    result = r.json().get("results")[0]
    file = result.get("cover").get("file")
    external = result.get("cover").get("external")
    if(not external is None):
        cover = external.get("url")
    elif(not file is None):
        cover = file.get("url")
    id = result.get("id")
    getPage(id,cover)
def getPage(id,cover):
    message =" "
    index = 1
    r = getContent(id)
    print(r.text)
    results = r.json().get("results")
    for result in results:
        type = result.get("type")
        text = result.get(type).get("text")
        checked = result.get(type).get("checked")
        if(type=="to_do" and not text is None and not checked):
            content =map[index]+" "+parseText(text)+"\n\n"
            message += content
            index+=1
    print(message)
    if index > 1:
        send(message,cover)
#获取内容
def getContent(id):
    r = requests.get('https://api.notion.com/v1/blocks/'+id+'/children',headers=headers)
    return r
#解析文本
def parseText(text):
    r = ''
    for t in text:
        content = t.get("text").get("content")
        link = t.get("text").get("link")
        content = content.replace(".","\.")
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
        if(not link is None):
            url = link.get("url")
            content = "["+content+"]("+url+")"
        r+=content
    return r
    
#创建markdown文件
def send(message,cover):
    url = "https://api.telegram.org/bot1756944825:AAHVzM7zWJ-QTwomwTOJrF08raPqVqhtQhc/sendPhoto"
    body = {
        "chat_id": "@xiaoma1989",
        "photo": cover,
        "caption":message,
        "parse_mode": "MarkdownV2"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.request("POST", url, headers=headers, json=body)
    print(r.text)
   

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("title")
    options = parser.parse_args()
    title = options.title
    if(len(title)==0):
        print("null")
        target = datetime.now()
    else:    
        target = datetime.strptime(title, '%Y%m%d')
    headers = {'Authorization': options.secret,"Notion-Version":options.version}
    search(target)
