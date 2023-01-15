import argparse
from datetime import date, datetime, timedelta
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
categories: [日记]
comment : true
---
"""

# 写前一天的
today = datetime.now()
yesterday = (today-timedelta(days=1)).strftime("%Y-%m-%dT23:30:00+08:00")
today = today.strftime("%Y-%m-%dT23:30:00+08:00")

filter = {"and": [
    {"property": "Date", "date": {"after": yesterday}},
    {"property": "Date", "date": {"before": today}},
]}


def query_day():
    response = notion_api.query_database("d34e3250832a4b5fb44054a8b364df2a")
    list = []
    for index in range(0, len(response.get("results"))):
        name = notion_api.get_title(response, "Name", index)
        day = notion_api.get_formula(response, "倒数日", index)
        progress = notion_api.get_formula(response, "Progress", index)
        list.append(name + day + " " + progress)
    return list


def query_ncm():
    response = notion_api.query_database(
        "46beb49d60b84317a0a2c36a0a024c71", filter=filter)
    if len(response.get("results")) > 0:
        return notion_api.get_rich_text(response, "id")
    return ''


def query_twitter():
    response = notion_api.query_database(
        "5351451787d9403fb48d9a9c20f31f43", filter)
    urls = []
    for index in range(0, len(response.get("results"))):
        id = notion_api.get_rich_text(response, "id", index)
        name = notion_api.get_title(response, "Name", index)
        urls.append(
            "{"+"""{{< tweet user="{name}" id="{id}" >}}""".format(name=name, id=id)+"}")
    return urls


def query_weight():
    response = notion_api.query_database(
        "34c0db4313b24c3fac8e25436f5b3530", filter)
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["体重"]["number"]
    return 0


def query_bilibili():
    response = notion_api.query_database(
        "de0b737abfd0490abd9e4652073becfe", filter)
    urls = []
    for result in response.get("results"):
        title = result["properties"]["Name"]["title"][0]["text"]["content"]
        url = result["properties"]["link"]["rich_text"][0]["text"]["content"]
        urls.append("[" + title + "](" + url + ")")
    return urls


def query_run():
    response = notion_api.query_database(
        "8dc2c4145901403ea9c4fb0b10ad3f86", filter)
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["距离"]["number"]
    return 0


def query_book():
    response = notion_api.query_database(
        "cca71ece15ac48a68c34e5f86a2e6b38", filter)
    results = response.get("results")
    if len(results) > 0:
        properties = results[0]['properties']
        name = properties['Name']['title'][0]['text']['content']
        duration = properties['时长']['number']
        return "读《" + name + "》" + str(duration) + " 分钟"
    return None


def query_todo():
    filter = {"and": [
        {"property": "Date", "date": {"after": yesterday}},
        {"property": "Date", "date": {"before": today}},
        {"property": "Status", "select": {"equals": "Completed"}},
    ]}
    response = notion_api.query_database(
        "97955f34653b4658bc0aaa50423be45f", filter)
    todo_list = []
    results = response.get("results")
    for result in results:
        todo_list.append(result['properties']['Title']
                         ['title'][0]['text']['content'])
    print(todo_list)
    return todo_list


def query_toggl():
    response = notion_api.query_database(
        "d8eee75d8c1049e7aa3dd6614907bb04", filter)
    toggl_list = []
    for index in range(0, len(response.get("results"))):
        date = notion_api.get_date(response, "Date", index)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(date.get("start")).strftime("%H:%M")
        end = datetime.fromisoformat(date.get("end")).strftime("%H:%M")
        name = notion_api.get_select(response, "二级分类", index)
        note = notion_api.get_rich_text(response, "备注", index)
        result = start + "-" + end + "：" + name
        if note != None and note != "":
            result += "，" + note
        toggl_list.append(result)
    return toggl_list


def create():
    response = notion_api.query_database(
        "294060cd-e13e-4c29-b0ac-6ee490c8a448", filter)
    cover = response.get("results")[0].get("cover").get("external").get("url")
    icon = response.get("results")[0].get("icon").get("emoji")
    name = notion_api.get_title(response, "Name")
    name = icon + " " + name
    tag = notion_api.get_multi_select(response, "Tag")
    items = []
    for item in tag:
        items.append(item.get("name"))
    location = notion_api.get_rich_text(response, "位置")
    result = template.format(
        title=name,
        date=notion_api.get_date(response, "Date").get("start"),
        location=location,
        tag=",".join(items),
        cover=cover,
    )
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
    song = query_ncm()
    if song != '':
        song_id = song.split('=')[1]
        result += '{{<aplayer server="netease" type="song" id="'+song_id+'">}}\n'
    days = query_day()
    if len(days) > 0:
        result += "## 📅 倒数日"
        result += "\n"
        for day in days:
            result += "- " + day
            result += "\n"
    result += "## ✅ ToDo"
    result += "\n"
    book = query_book()
    if book is not None:
        result += "- [x] " + book
        result += "\n"
    todos = query_todo()
    for todo in todos:
        result += "- [x] " + todo
        result += "\n"
    result += "## ❤️ 健康"
    result += "\n"
    weight = query_weight()
    if weight > 0:
        result += "- 体重：" + str(weight) + "斤"
        result += "\n"
    run = query_run()
    if run > 0:
        result += "- 跑步：" + str(run) + "km"
        result += "\n"
    result += "## ⏰ 时间统计"
    result += "\n"
    toggls = query_toggl()
    for toggl in toggls:
        result += "- " + toggl
        result += "\n"
    urls = query_twitter()
    if len(urls) > 0:
        result += "## 💬 碎碎念"
        result += "\n"
        for url in urls:
            result += url
            result += "\n"
    urls = query_bilibili()
    if len(urls) > 0:
        result += "\n"
        result += "## 📺 今天看了啥"
        result += "\n"
        for url in urls:
            result += "- "+url
            result += "\n"
    file = datetime.strftime(datetime.now(), "%Y-%m-%d") + ".md"
    with open("./content/posts/" + file, "w") as f:
        f.seek(0)
        f.write(result)
        f.truncate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    create()
