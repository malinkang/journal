import argparse
from datetime import date, datetime, timedelta
import os
import time
import notion_api
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties
import util
from config import (
    MOVIE_DATABASE_ID,
    BOOK_DATABASE_ID,
    DAY_PAGE_ID,
    TOGGL_DATABASE_ID, TODO_DATABASE_ID
)
template = """
---
title: "{title}"
date: {date}
description: "{location}"
tags: [{tag}]
featured_image: "{cover}"
categories: [日记]
comment : true
---
"""


def query_day():
    time.sleep(0.3)
    response = notion_api.query_database("d34e3250832a4b5fb44054a8b364df2a")
    list = []
    for result in response.get("results"):
        name = util.get_title(result, "Name")
        day = util.get_formula(result, "倒数日")
        progress = util.get_formula(result, "Progress")
        list.append(name + day + " " + progress)
    return list


def query_ncm():
    time.sleep(0.3)
    response = notion_api.query_database(
        "46beb49d60b84317a0a2c36a0a024c71", filter=get_filter())
    if len(response.get("results")) > 0:
        return util.get_rich_text(response.get("results")[0], "id")
    return ''


def query_twitter():
    time.sleep(0.3)
    response = notion_api.query_database(
        "5351451787d9403fb48d9a9c20f31f43", get_filter())
    urls = []
    for result in response.get("results"):
        id = util.get_rich_text(result,"id")
        name = util.get_title(result,"Name")
        text = util.get_rich_text(result,"text")
        if id == None or id =='':
            urls.append(f"* {text}")
        else:
            urls.append(
                "{"+"""{{< tweet user="{name}" id="{id}" >}}""".format(name=name, id=id)+"}")
    return urls


def query_weight():
    time.sleep(0.3)
    response = notion_api.query_database(
        "34c0db4313b24c3fac8e25436f5b3530", get_filter())
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["体重"]["number"]
    return 0


def query_bilibili():
    time.sleep(0.3)
    response = notion_api.query_database(
        "de0b737abfd0490abd9e4652073becfe", get_filter())
    urls = set()
    for result in response.get("results"):
        title = result["properties"]["Name"]["title"][0]["text"]["content"]
        url = result["properties"]["Url"]["url"]
        urls.add("[" + title + "](" + url + ")")
    return urls


def get_filter( name="Date", extras=[]):
    """
    date：时间
    name：属性名称
    extras：额外的条件
    """
    start = date.strftime("%Y-%m-%dT00:00:00+08:00")
    end = date.strftime("%Y-%m-%dT24:00:00+08:00")
    conditions = [
        {"property": name, "date": {"on_or_after": start}},
        {"property": name, "date": {"on_or_before": end}},
    ]
    if (len(extras) > 0):
        conditions.extend(extras)
    filter = {"and": conditions}
    return filter


def query_movie():
    time.sleep(0.3)
    filter = get_filter(name="打分日期")
    response = notion_api.query_database(MOVIE_DATABASE_ID, filter)
    urls = set()
    for result in response.get("results"):
        title = result["properties"]["标题"]["title"][0]["text"]["content"]
        url = result["properties"]["条目链接"]["url"]
        status = result["properties"]["状态"]["select"]["name"]
        urls.add(f"[{status}{title}]({url})")
    return urls


def query_tv():
    time.sleep(0.3)
    filter = get_filter(name="Date")
    response = notion_api.query_database("301da784bddd41b692ee711e08150487", filter)
    urls = set()
    for result in response.get("results"):
        title = result["properties"]["Name"]["title"][0]["text"]["content"]
        url = result["properties"]["URL"]["url"]
        season = result["properties"]["Season"]["number"]
        number = result["properties"]["Number"]["number"]
        urls.add(f"看过[{title}]({url})第{season}季第{number}集")
    return urls


def query_run():
    time.sleep(0.3)
    response = notion_api.query_database(
        "8dc2c4145901403ea9c4fb0b10ad3f86", get_filter())
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["距离"]["number"]
    return 0

def query_book():
    time.sleep(0.3)
    response = notion_api.query_database(
        "cca71ece15ac48a68c34e5f86a2e6b38", get_filter())
    books = set()
    for result in response.get("results"):
        properties = result['properties']
        name = properties['Name']['title'][0]['text']['content']
        duration = properties['时长']['number']
        url = properties['URL']['url']
        books.add(f"读[《{name}》]({url}){duration}分钟")
    return books

def query_douban_book():
    time.sleep(0.3)
    books = set()
    response = notion_api.query_database(BOOK_DATABASE_ID, get_filter(name="打分日期"))
    for result in response.get("results"):
        title = result["properties"]["标题"]["title"][0]["text"]["content"]
        url = result["properties"]["条目链接"]["url"]
        status = result["properties"]["状态"]["select"]["name"]
        books.add(f"[{status}{title}]({url})")
    return books


def query_todo():
    """查询今日完成的任务"""
    time.sleep(0.3)
    extras = [{"property": "Status", "status": {"equals": "Completed"}}]
    response = notion_api.query_database(TODO_DATABASE_ID, get_filter(extras=extras))
    return [result['properties']['Title']['title'][0]['text']['content'] for result in response.get("results")]


def query_toggl():
    #前天的20点到昨天的8点 搜索睡觉事件
    time.sleep(0.3)
    yesterday = (date-timedelta(days=1)).strftime("%Y-%m-%dT20:00:00+08:00")
    today = date.strftime("%Y-%m-%dT08:00:00+08:00")
    filter = {
        "and": [
            {"property": "Date", "date": {"after": yesterday}},
            {"property": "Date", "date": {"before": today}},
            {"property": "二级分类", "select": {"equals": "😴睡觉"}}
        ]
    }
    response = notion_api.query_database(TOGGL_DATABASE_ID, filter)
    start =  date.strftime("%Y-%m-%dT00:00:00+08:00")
    end =  date.strftime("%Y-%m-%dT24:00:00+08:00")
    if len(response.get("results")) > 0:
        start = response["results"][0]["properties"]["Date"]["date"]["start"]
    print(start)
    filter = {
        "and": [
            {"property": "Date", "date": {"on_or_after": start}},
            {"property": "Date", "date": {"on_or_before": end}},
        ]
    }
    sorted = [
        {
            "property": "Date",
            "direction": "ascending"
        }
    ]
    response = notion_api.query_database(TOGGL_DATABASE_ID, filter,sorted)
    toggl_list = []
    for index in range(0, len(response.get("results"))):
        d = notion_api.get_date(response, "Date", index)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(d.get("start")).strftime("%H:%M")
        end = datetime.fromisoformat(d.get("end")).strftime("%H:%M")
        name = notion_api.get_select(response, "二级分类", index)
        note = notion_api.get_rich_text(response, "备注", index)
        result = start + "-" + end + "：" + name
        if note != None and note != "":
            result += "：" + note
        toggl_list.append(result)
    return toggl_list


def create():
    response = notion_api.query_database(DAY_PAGE_ID, get_filter())
    results = response.get("results")
    for result in results:
        cover = result.get("cover").get("external").get("url")
        icon = result.get("icon").get("emoji")
        name = util.get_title(result, "Name")
        name = icon + " " + name
        tags = util.get_multi_select(result, "Tags")
        items = []
        for item in tags:
            items.append(item.get("name"))
        location = util.get_rich_text(result, "位置")
        r = template.format(
            title=name,
            date=util.get_date(result, "Date"),
            location=location,
            tag=",".join(items),
            cover=cover,
        )
        r += "\n"
        content = ""
        song = query_ncm()
        if song != '':
            r += '{{<spotify type="track" id="'+song+'" width="100%" height="100" >}}\n'
        weather = util.get_rich_text(result, "天气")
        if weather is not None:
            content += "今天天气" + weather
        aq = util.get_number(result, "空气质量")
        if weather is not None:
            content += "，空气质量" + str(aq)
        highest = util.get_rich_text(result, "最高温度")
        if highest is not None:
            content += "，最高温度" + highest
        lowest = util.get_rich_text(result, "最低温度")
        if lowest is not None:
            content += "，最低温度" + lowest
        if content == "":
            pass
        else:
            content += "。"
        r += content
        r += "\n"
        days = query_day()
        if len(days) > 0:
            r += "## 📅 倒数日"
            r += "\n"
            for day in days:
                r += "- " + day
                r += "\n"
        r += "## ✅ ToDo"
        r += "\n"
        todos = query_todo()
        for todo in todos:
            r += "- [x] " + todo
            r += "\n"
        r += "## ❤️ 健康"
        r += "\n"
        weight = query_weight()
        if weight > 0:
            r += "- 体重：" + str(weight) + "斤"
            r += "\n"
        run = query_run()
        if run > 0:
            r += "- 跑步：" + str(run) + "km"
            r += "\n"
        r += "## ⏰ 时间统计"
        r += "\n"
        toggls = query_toggl()
        for toggl in toggls:
            r += "- " + toggl
            r += "\n"
        urls = query_twitter()
        if len(urls) > 0:
            r += "## 💬 碎碎念"
            r += "\n"
            for url in urls:
                r += url
                r += "\n"
        urls = query_bilibili() | query_movie() | query_tv()
        if len(urls) > 0:
            r += "\n"
            r += "## 📺 今天看了啥"
            r += "\n"
            for url in urls:
                r += "- "+url
                r += "\n"
        books = query_book() | query_douban_book()
        if len(books) > 0:
            r += "\n"
            r += "## 📚 读书"
            r += "\n"
            for url in books:
                r += "- "+url
                r += "\n"
        dir = "./content/posts/" + datetime.strftime(date, "%Y")+"/"+datetime.strftime(date,"%Y-%m-%d")
        if os.path.exists(dir+"/images") and len(os.listdir(dir+"/images")) > 0:
            r += "\n"
            r += "## 📷 照片"
            r += "\n"
            r += '{{< gallery match="images/*" sortOrder="desc" rowHeight="150" margins="5" thumbnailResizeOptions="600x600 q90 Lanczos" showExif=true previewType="blur" embedPreview=true loadJQuery=true >}}'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = dir+ "/index.md"
        with open(file, "w") as f:
            f.seek(0)
            f.write(r)
            f.truncate()

date = datetime.now()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    content = parser.parse_args().content
    if content !="":
       date = datetime.strptime(parser.parse_args().content, "%Y-%m-%d")
    options = parser.parse_args()
    create()
