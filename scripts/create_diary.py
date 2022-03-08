#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, datetime
import requests
import argparse

import unsplash
import notion
from datetime import datetime, timedelta

from requests.api import get


week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}


# 创建Page
def create_page(pageId):
    emo = "☀️"
    tomorrow = datetime.now() + timedelta(days=1)
    week = tomorrow.strftime("%V")
    month = tomorrow.month
    title = datetime.strftime(tomorrow, "%m月%d日 星期" + week_day_dict[tomorrow.weekday()])
    children = []

    children.append(notion.get_heading_2("✅ TODO"))
    for todo in getTodo():
        children.append(todo)
    children.append(notion.get_divider())
    children.append(notion.get_heading_2("💬 碎碎念"))
    children.append(notion.get_divider())
    children.append(notion.get_heading_2("📅 今日日程"))
    cover = unsplash.random()
    properties = {
        "title": {"title": [{"type": "text", "text": {"content": title}}]},
        "日期": {"date": {"start": datetime.strftime(tomorrow, "%Y-%m-%d")}},
        "标签": {
            "type": "multi_select",
            "multi_select": [
                {"name": str(month) + "月"},
                {"name": "第" + week + "周"},
            ],
        },
    }
    properties = notion.get_relation(properties,tomorrow,False)
    body = {
        "parent": {"database_id": pageId},
        "properties": properties,
        "cover": {"type": "external", "external": {"url": cover}},
        "icon": {"type": "emoji", "emoji": emo},
        "children": children,
    }

    r = requests.post("https://api.notion.com/v1/pages/", headers=headers, json=body)
    print(r.text)


def getTodo():
    todo = []
    tomorrow = datetime.now() + timedelta(days=1)
    day = tomorrow.day
    week = tomorrow.weekday()

    if week < 7:
        todo.append(notion.get_todo("🍚 订餐", "https://meican.com/"))
        todo.append(notion.get_todo("💰 打新", "https://meican.com/"))
        if week == 4:
            todo.append(notion.get_todo("💰 定投"))
    if day == 8 or day == 6 or day == 21:
        todo.append(notion.get_todo("💳  信用卡还款"))
    todo.append(notion.get_todo("🏃🏻 步数打卡"))
    return todo


headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("id")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    headers = {"Authorization": options.secret, "Notion-Version": options.version}
    create_page(options.id)
