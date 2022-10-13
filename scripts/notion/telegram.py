import argparse
from datetime import date, datetime, timedelta
from unittest import result

import requests
import notion_api
import dateutils
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties

template = """
---
title: "{title}"
date: {date}
description: "{location}"
tags: [{tag}]
featured_image: "{cover}"
categories: ["日记"]
comment : false
---
"""


today = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%dT00:00:00+08:00")


def query_day():
    response = notion_api.query_database("d34e3250832a4b5fb44054a8b364df2a")
    list = []
    for index in range(0, len(response.get("results"))):
        name = notion_api.get_title(response, "Name", index)
        day = notion_api.get_formula(response, "倒数日", index)
        progress = notion_api.get_formula(response, "Progress", index)
        list.append(name + day + " " + progress)
    return list


def query_twitter():
    filter = {"property": "Date", "date": {"after": today}}
    response = notion_api.query_database("5351451787d9403fb48d9a9c20f31f43", filter)
    urls = []
    for index in range(0, len(response.get("results"))):
        text = notion_api.get_rich_text(response, "text", index)
        url = notion_api.get_by_type(response, "url","url", index)
        urls.append("[" + text + "](" + url + ")")
    return urls


def query_weight():
    filter = {"property": "Date", "date": {"after": today}}
    response = notion_api.query_database("34c0db4313b24c3fac8e25436f5b3530", filter)
    if len(response.get("results")) > 0:
        return notion_api.get_number(response, "体重")
    return 0


def query_book():
    filter = {"property": "Date", "date": {"after": today}}
    response = notion_api.query_database("cca71ece15ac48a68c34e5f86a2e6b38", filter)
    results = response.get("results")
    if len(results) > 0:
        properties = results[0]['properties']
        name = properties['Name']['title'][0]['text']['content']
        duration =properties['时长']['number']
        return "读《" + name + "》" + str(duration) + " 分钟"
    return None


def query_todo():
    filter = {"property": "Date", "date": {"after": today}}
    response = notion_api.query_database("97955f34653b4658bc0aaa50423be45f", filter)
    todo_list = []
    if len(response.get("results")) > 0:
        todo_list.append(notion_api.get_title(response, "Name"))
    return todo_list


def query_toggl():
    yesteday =datetime.now()-timedelta(days=2)
    yesteday = yesteday.replace(hour=23).replace(minute=30).replace(second=0).replace(microsecond=0)
    yesteday = yesteday.isoformat()
    yesteday+="+08:00"
    filter = {"property": "Date", "date": {"after": yesteday}}
    response = notion_api.query_database("d8eee75d8c1049e7aa3dd6614907bb04", filter)
    toggl_list = []
    for index in range(0, len(response.get("results"))):
        date = notion_api.get_date(response, "Date", index)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(date.get("start")).strftime("%H:%M")
        end = datetime.fromisoformat(date.get("end")).strftime("%H:%M")
        name = notion_api.get_select(response, "二级分类", index)
        note = notion_api.get_rich_text(response, "备注", index)
        result = start + "-" + end + "：" + name
        if note is not None and note is not "":
            result += "，" + note
        toggl_list.append(result)
    return toggl_list


def create():
    title = dateutils.format_date_with_week()
    filter = {"property": "Name", "rich_text": {"equals": title}}
    response = notion_api.query_database("294060cd-e13e-4c29-b0ac-6ee490c8a448", filter)
    cover = response.get("results")[0].get("cover").get("external").get("url")
    icon = response.get("results")[0].get("icon").get("emoji")
    name = notion_api.get_title(response, "Name")
    name = icon +" "+ name
    tags = notion_api.get_multi_select(response, "Tag")
    tags = " ".join("#"+tag.get("name")for tag in tags)
    result = name
    result += "\n"
    content = ""
    weather = notion_api.get_rich_text(response, "天气")
    if weather is not None:
        content += "今天天气" + weather
    aq = notion_api.get_number(response, "空气质量")
    if weather is not None:
        content += "，空气质量" + str(aq)
    highest = notion_api.get_rich_text(response, "最高温度")
    if highest is not None:
        content += "，最高温度" + highest
    lowest = notion_api.get_rich_text(response, "最低温度")
    if lowest is not None:
        content += "，最低温度" + lowest
    if content == "":
        pass
    else:
        content += "。"
    result += content
    result += "\n"
    days = query_day()
    if len(days) > 0:
        result += "\n"
        result += "*📅 倒数日*"
        result += "\n"
        for day in days:
            result += "- " + day
            result += "\n"
    result += "\n"
    result += "*✅ ToDo*"
    result += "\n"
    book = query_book()
    if book is not None:
        result += "- [x] " + book
        result += "\n"
    todos = query_todo()
    for todo in todos:
        result += "- [x] " + todo
        result += "\n"
    result += "\n"
    result += "*❤️ 健康*"
    result += "\n"
    weight = query_weight()
    if weight is not None:
        result += "- 体重：" + str(weight)+ "斤"
        result += "\n"
    result += "\n"
    result += "*⏰ 时间统计*"
    result += "\n"
    toggls = query_toggl()
    for toggl in toggls:
        result += "- " + toggl
        result += "\n"

    urls = query_twitter()
    if len(urls) > 0:
        result += "\n"
        result +="*💬 碎碎念*"
        result += "\n"
        for url in urls:
            result += "- "+url
            result += "\n"
    result += "\n"
    result += tags
    result = result.replace('.','\.')
    result = result.replace('-','\-')
    result = result.replace('[x]','\[x\]')
    result = result.replace('#','\#')
    send(result,cover)
def send(message,cover):
    url = "https://api.telegram.org/bot5509900379:AAHSimr7FiKrclApJImy91A3Dff4R4g2OPk/sendPhoto"
    print(message)
    body = {
        "chat_id": "@xiaoma2023",
        "photo": cover,
        "caption":message,
        "parse_mode": "MarkdownV2"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.request("POST", url, headers=headers, json=body)
    print(r.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    create()
    # print(query_twitter())