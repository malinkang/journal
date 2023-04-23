import argparse
from datetime import date, datetime, timedelta

import requests
import notion_api
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties
import util
from config import (
    MOVIE_DATABASE_ID,
    DAY_PAGE_ID,
    TOGGL_DATABASE_ID, TODO_DATABASE_ID
)

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
        "46beb49d60b84317a0a2c36a0a024c71", filter=get_filter())
    if len(response.get("results")) > 0:
        return notion_api.get_rich_text(response, "id")
    return ''


def query_twitter():
    response = notion_api.query_database(
        "5351451787d9403fb48d9a9c20f31f43", get_filter())
    urls = []
    for result in response.get("results"):
        id = util.get_rich_text(result,"id")
        text = util.get_rich_text(result,"text")
        url = result["properties"]["url"]["url"]
        if id == None or id =='':
            urls.append(text)
        else:
            urls.append(
                f"[{text}]({url})")
    return urls


def query_weight():
    response = notion_api.query_database(
        "34c0db4313b24c3fac8e25436f5b3530", get_filter())
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["体重"]["number"]
    return 0


def query_bilibili():
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
    filter = get_filter(name="打分日期")
    response = notion_api.query_database(MOVIE_DATABASE_ID, filter)
    urls = set()
    for result in response.get("results"):
        title = result["properties"]["标题"]["title"][0]["text"]["content"]
        url = result["properties"]["条目链接"]["url"]
        status = result["properties"]["状态"]["select"]["name"]
        urls.add(f"[{status}{title}]({url})")
    return urls


def query_run():
    response = notion_api.query_database(
        "8dc2c4145901403ea9c4fb0b10ad3f86", get_filter())
    results = response.get("results")
    if len(results) > 0:
        return results[0]["properties"]["距离"]["number"]
    return 0


def query_book():
    response = notion_api.query_database(
        "cca71ece15ac48a68c34e5f86a2e6b38", get_filter())
    books = []
    for result in response.get("results"):
        properties = result['properties']
        name = properties['Name']['title'][0]['text']['content']
        duration = properties['时长']['number']
        url = properties['URL']['url']
        books.append(f"读[《{name}》]({url}){duration}分钟")
    return books


def query_todo():
    """查询今日完成的任务"""
    print(get_filter())
    extras = [{"property": "Status", "status": {"equals": "Completed"}}]
    response = notion_api.query_database(TODO_DATABASE_ID, get_filter(extras=extras))
    return [result['properties']['Title']['title'][0]['text']['content'] for result in response.get("results")]


def query_toggl():
    #前天的20点到昨天的8点 搜索睡觉事件
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

date = datetime.now()
def create():
    response = notion_api.query_database(DAY_PAGE_ID, get_filter())
    cover = response.get("results")[0].get("cover").get("external").get("url")
    icon = response.get("results")[0].get("icon").get("emoji")
    name = notion_api.get_title(response, "Name")
    name = icon +" "+ name
    tags = notion_api.get_multi_select(response, "Tags")
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
    books = query_book()
    if len(books) > 0:
            result += "\n"
            result += "## 📚 今天读了啥"
            result += "\n"
            for url in books:
                result += "- "+url
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
    urls  = query_bilibili()
    if len(urls) > 0:
        result += "\n"
        result +="*📺 今天看了啥*"
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
    result = result.replace('|','\|')
    send(result,cover)
def send(message,cover):
    url = "https://api.telegram.org/bot5509900379:AAHSimr7FiKrclApJImy91A3Dff4R4g2OPk/sendPhoto"
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