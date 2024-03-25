import argparse
from datetime import date, datetime, timedelta
import glob
import os
import time

import pendulum
import notion_api
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties
import util
from config import (
    MOVIE_DATABASE_ID,
    BOOK_DATABASE_ID,
    DAY_PAGE_ID,
    TOGGL_DATABASE_ID,
    TODO_DATABASE_ID,
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
    response = notion_api.query_database(database_id="d34e3250832a4b5fb44054a8b364df2a")
    list = []
    for result in response.get("results"):
        print(result)
        name = util.get_title(result, "Name")
        day = util.get_formula(result, "倒数日")
        progress = util.get_formula(result, "Progress")
        print(f"name = {name} day = {day} progress = {progress}")
        list.append(name + day + " " + progress)
    return list


def query_duolingo():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="8dc983cda135457fb65204ad62dd5f94", filter=get_filter(name="日期")
    )
    list = []
    for result in response.get("results"):
        xp = util.get_number(result, "经验")
        duration = int(round((util.get_number(result, "学习时长") / 60), 0))
        session = util.get_number(result, "单元")
        list.append(f"今天在多邻国学习了{duration}分钟，完成了{session}单元，共获得{xp}经验")
    return list


def query_ncm():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="46beb49d60b84317a0a2c36a0a024c71", filter=get_filter()
    )
    if len(response.get("results")) > 0:
        return util.get_rich_text(response.get("results")[0], "id")
    return ""


def query_twitter():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="5351451787d9403fb48d9a9c20f31f43", filter=get_filter()
    )
    urls = []
    for result in response.get("results"):
        id = util.get_rich_text(result, "id")
        name = util.get_title(result, "Name")
        text = util.get_rich_text(result, "text")
        type = util.get_select(result, "Type")
        if id == None or id == "":
            urls.append(f"* {text}")
        if type == "mastodon":
            urls.append("{" + """{{< mastodon status="{id}" >}}""".format(id=id) + "}")
        else:
            urls.append(
                "{"
                + """{{< tweet user="{name}" id="{id}" >}}""".format(name=name, id=id)
                + "}"
            )
    return urls


def query_weight():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="34c0db4313b24c3fac8e25436f5b3530",filter=get_filter()
    )
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["体重"]["number"]
    return 0


def query_bilibili():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="de0b737abfd0490abd9e4652073becfe", filter=get_filter()
    )
    urls = set()
    for result in response.get("results"):
        title = result["properties"]["Name"]["title"][0]["text"]["content"]
        url = result["properties"]["Url"]["url"]
        urls.add("[" + title + "](" + url + ")")
    return urls


def get_filter(name="Date", extras=[]):
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
    if len(extras) > 0:
        conditions.extend(extras)
    filter = {"and": conditions}
    print(filter)
    return filter

#https://www.notion.so/malinkang/4647d31ae4a44d06a155fcf7143c382e?v=b0d70b0fdb3e4f809b461c692cdbde44&pvs=4
def query_movie():
    time.sleep(0.3)
    response = notion_api.query_database(database_id="4647d31ae4a44d06a155fcf7143c382e", filter=get_filter(name="日期"))
    urls = set()
    for result in response.get("results"):
        title = util.get_title(result,"电影名")
        url = util.get_url(result,"豆瓣链接")
        status = result["properties"]["状态"]["status"]["name"]
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
    list = []
    response = notion_api.query_database(
        database_id="8dc2c4145901403ea9c4fb0b10ad3f86", filter=get_filter()
    )
    results = response.get("results")
    for result in results:
        id = util.get_rich_text(result, "id")
        km = results[0]["properties"]["KM"]["formula"]["number"]
        list.append(f"- 跑步：[{km}km](https://www.strava.com/activities/{id})")
    return list


def query_book():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="cca71ece15ac48a68c34e5f86a2e6b38", filter=get_filter()
    )
    books = set()
    for result in response.get("results"):
        properties = result["properties"]
        name = properties["Name"]["title"][0]["text"]["content"]
        duration = properties["时长"]["number"]
        url = properties["URL"]["url"]
        books.add(f"读[《{name}》]({url}){duration}分钟")
    return books

#https://www.notion.so/malinkang/8db320a226324aa1a20ed7bbc39b7727?v=01e5a358c0f64da19a66dbe220c2ce5f&pvs=4
def query_douban_book():
    time.sleep(0.3)
    books = set()
    response = notion_api.query_database(database_id="8db320a226324aa1a20ed7bbc39b7727", filter=get_filter(name="日期"))
    for result in response.get("results"):
        title = util.get_title(result,"书名")
        url = util.get_url(result,"豆瓣链接")
        status = result["properties"]["状态"]["status"]["name"]
        books.add(f"[{status}{title}]({url})")
    return books

def query_todo():
    """查询今日完成的任务"""
    time.sleep(0.3)
    extras = [{"property": "状态", "status": {"equals": "Completed"}}]
    response = notion_api.query_database(database_id=TODO_DATABASE_ID, filter=get_filter(name="完成时间",extras=extras))
    return [
        result["properties"]["Title"]["title"][0]["text"]["content"]
        for result in response.get("results")
    ]


# https://www.notion.so/malinkang/cf6359306f94456da01908af73191a61?v=462ad72e1a4c4c3591a074816dcccbd1&pvs=4
def query_toggl():
#     # 前天的20点到昨天的8点 搜索睡觉事件
    start = (pendulum.now(tz="Asia/Shanghai")-timedelta(days=1)).strftime("%Y-%m-%dT00:00:00+08:00")
    end = date.strftime("%Y-%m-%dT24:00:00+08:00")
    filter = {
        "and": [
            {"property": "时间", "date": {"on_or_after": start}},
            {"property": "时间", "date": {"on_or_before": end}},
        ]
    }
    sorted = [{"property": "时间", "direction": "ascending"}]
    response = notion_api.query_database(database_id="cf6359306f94456da01908af73191a61", filter=filter, sorted=sorted)
    toggl_list = []
    for result in response.get("results"):
        start,end = util.get_date(result, "时间")
        emoji = util.get_icon(result)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(start).strftime("%H:%M")
        end = datetime.fromisoformat(end).strftime("%H:%M")
        name = util.get_title(result, "标题")
        note = util.get_rich_text(result, "备注")
        result = f'{start}-{end}：{emoji} {name}'
        if note != None and note != "":
            result += "：" + note
        toggl_list.append(result)
    return toggl_list


def create():
    response = notion_api.query_database(database_id=DAY_PAGE_ID, filter=get_filter())
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
            date=util.get_date(result, "Date")[0],
            location=location,
            tag=",".join(items),
            cover=cover,
        )
        r += "\n"
        content = ""
        song = query_ncm()
        if song != "":
            r += (
                '{{<spotify type="track" id="'
                + song
                + '" width="100%" height="100" >}}\n'
            )
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
        if len(run) > 0:
            r += "\n".join(run)
            r += "\n"
        duolingo = query_duolingo()
        if len(duolingo) > 0:
            r += "## 📖 学习\n"
            r += "\n".join(duolingo)
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
        urls = query_bilibili() | query_movie()
        if len(urls) > 0:
            r += "\n"
            r += "## 📺 今天看了啥"
            r += "\n"
            for url in urls:
                r += "- " + url
                r += "\n"
        books = query_book() | query_douban_book()
        if len(books) > 0:
            r += "\n"
            r += "## 📚 读书"
            r += "\n"
            for url in books:
                r += "- " + url
                r += "\n"
        if os.path.exists(dir + "/images") and len(os.listdir(dir + "/images")) > 0:
            r += "\n"
            r += "## 📷 照片"
            r += "\n"
            r += '{{< gallery match="images/*" sortOrder="desc" rowHeight="150" margins="5" thumbnailResizeOptions="600x600 q90 Lanczos" showExif=true previewType="blur" embedPreview=true loadJQuery=true >}}'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = dir + "/index.md"
        with open(file, "w") as f:
            f.seek(0)
            f.write(r)
            f.truncate()


date = datetime.now()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    content = parser.parse_args().content
    if content != "":
        date = datetime.strptime(parser.parse_args().content, "%Y-%m-%d")
    options = parser.parse_args()
    year = datetime.strftime(date, "%Y")
    month = datetime.strftime(date, "%m")
    day = datetime.strftime(date, "%d")
    dir = f"./content/posts/{year}/{year}-{month}-{day}/"
    create()
    # print(query_duoligo())
    # query_twitter()
    # query_run()
    # print(query_memos())
    # print(query_toggl())
    # print(query_movie())
