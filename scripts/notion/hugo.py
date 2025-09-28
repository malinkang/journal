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
        database_id="e646426349a3449eacbc30e9e71ce33b", filter=get_filter(name="日期")
    )
    list = []
    for result in response.get("results"):
        xp = util.get_number(result, "经验")
        duration = int(round((util.get_number(result, "学习时长") / 60), 0))
        session = util.get_number(result, "单元")
        list.append(
            f"今天在多邻国学习了{duration}分钟，完成了{session}单元，共获得{xp}经验"
        )
    return list


def query_music():
    response = notion_api.query_database(
        database_id="f852878351c7450db17f85b68410ce44", filter=get_filter("日期")
    )
    if len(response.get("results")) > 0:
        return response.get("results")[0].get("id")
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


def query_memos():
    response = notion_api.query_database(
        database_id="736d23cc9ef94bac865cfc9f6393e5d1", filter=get_filter(name="日期")
    )
    markdown_result = ""
    for result in response.get("results"):
        page_id = result.get("id")
        id = util.get_rich_text(result, "id")
        blocks = notion_api.get_all_blocks(page_id)
        images = []
        for block in blocks:
            block_type = block.get("type")
            if block_type == "image":
                url = block.get("image", {}).get("external", {}).get("url", "")
                images.append(url)
                download_image(url, f"{dir}/images/{id}/")
            else:
                markdown_result += notion_block_to_markdown(block)
        print(images)
        if images:
            markdown_result += f'{{{{< gallery match="images/{id}/*" sortOrder="desc" rowHeight="200" margins="5" thumbnailResizeOptions="600x600 q90 Lanczos" showExif=true previewType="blur" embedPreview=true loadJQuery=true >}}}}\n'
        markdown_result += "\n--------\n"
    return markdown_result


def download_image(url, parent_folder):
    import os
    import requests

    # 创建多级文件夹
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    # 获取图片内容
    response = requests.get(url)
    if response.status_code == 200:
        # 提取文件名
        file_name = os.path.join(parent_folder, url.split("/")[-1])
        # 写入文件
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"图片已下载到: {file_name}")
    else:
        print(f"无法下载图片，状态码: {response.status_code}")


def query_weight():
    time.sleep(0.3)
    response = notion_api.query_database(
        database_id="34c0db4313b24c3fac8e25436f5b3530", filter=get_filter()
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


# https://www.notion.so/malinkang/4647d31ae4a44d06a155fcf7143c382e?v=b0d70b0fdb3e4f809b461c692cdbde44&pvs=4
def query_movie():
    response = notion_api.query_database(
        database_id="aaa0f16646be480b8ad31c244f30ed17", filter=get_filter(name="日期")
    )
    urls = set()
    for result in response.get("results"):
        title = util.get_title(result, "电影名")
        url = util.get_url(result, "豆瓣链接")
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
    response = notion_api.query_database(
        database_id="25386019c92c81fd839cc2e903edd9e0", filter=get_filter(name="日期")
    )
    books = []
    for result in response.get("results"):
        properties = result.get("properties")
        duration = util.get_number(result, "时长")
        if properties.get("书架").get("relation"):
            book = notion_api.client.pages.retrieve(
                page_id=properties.get("书架").get("relation")[0].get("id")
            )
            name = util.get_title(book, "书名")
            print(name)
            url = util.get_url(book, "链接")
            books.append(f"读[《{name}》]({url}){round(duration/60)}分钟")
    return books


# https://www.notion.so/malinkang/8db320a226324aa1a20ed7bbc39b7727?v=01e5a358c0f64da19a66dbe220c2ce5f&pvs=4
# def query_douban_book():
#     books = set()
#     response = notion_api.query_database(
#         database_id="8db320a226324aa1a20ed7bbc39b7727", filter=get_filter(name="日期")
#     )
#     for result in response.get("results"):
#         title = util.get_title(result, "书名")
#         url = util.get_url(result, "豆瓣链接")
#         status = result["properties"]["状态"]["status"]["name"]
#         books.add(f"[{status}{title}]({url})")
#     return books


def query_todo():
    """查询今日完成的任务"""
    time.sleep(0.3)
    extras = [{"property": "状态", "status": {"equals": "Done"}}]
    response = notion_api.query_database(
        database_id=TODO_DATABASE_ID, filter=get_filter(name="完成时间", extras=extras)
    )
    return [
        result["properties"]["标题"]["title"][0]["text"]["content"]
        for result in response.get("results")
    ]


# https://www.notion.so/malinkang/cf6359306f94456da01908af73191a61?v=462ad72e1a4c4c3591a074816dcccbd1&pvs=4
def query_toggl():
    start = date.strftime("%Y-%m-%dT00:00:00+08:00")
    end = date.strftime("%Y-%m-%dT24:00:00+08:00")
    filter = {
        "and": [
            {"property": "时间", "date": {"on_or_after": start}},
            {"property": "时间", "date": {"on_or_before": end}},
        ]
    }
    sorted = [{"property": "时间", "direction": "ascending"}]
    response = notion_api.query_database(
        database_id="cf6359306f94456da01908af73191a61", filter=filter, sorted=sorted
    )
    results = ""
    if response.get("results"):
        results += "|  时间   |   分类  | 时长   | 备注    |\n"
        results += "|--------|--------|--------|--------|\n"
    for result in response.get("results"):
        start, end = util.get_date(result, "时间")
        emoji = util.get_icon(result)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(start).strftime("%H:%M")
        end = datetime.fromisoformat(end).strftime("%H:%M")
        name = util.get_title(result, "标题")
        duration = result.get("properties").get("时长格式化").get("formula").get("string")
        note = util.get_rich_text(result, "备注")
        results += f"|{start}-{end}|{emoji} {name}|{duration}|{note}|\n"
    return results


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
        song = query_music()
        if song:
            r += '{{<aplayer  server="notion" type="song" id="' + song + '">}}\n'
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
        if toggls:
            r += toggls
        urls = query_twitter()
        memos = query_memos()
        if urls or memos:
            r += "## 💬 碎碎念\n"
        if urls:
            r += "\n"
            for url in urls:
                r += url
                r += "\n"
        if memos:
            r += memos
        # urls = query_bilibili() | query_movie()
        urls = query_bilibili() 
        if len(urls) > 0:
            r += "\n"
            r += "## 📺 今天看了啥"
            r += "\n"
            for url in urls:
                r += "- " + url
                r += "\n"
        books = query_book()
        if books:
            r += "\n"
            r += "## 📚 读书"
            r += "\n"
            for url in books:
                r += "- " + url
                r += "\n"
        # if os.path.exists(dir + "/images") and len(os.listdir(dir + "/images")) > 0:
        #     r += "\n"
        #     r += "## 📷 照片"
        #     r += "\n"
        #     r += '{{< gallery match="images/*" sortOrder="desc" rowHeight="150" margins="5" thumbnailResizeOptions="600x600 q90 Lanczos" showExif=true previewType="blur" embedPreview=true loadJQuery=true >}}'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = dir + "/index.md"
        with open(file, "w") as f:
            f.seek(0)
            f.write(r)
            f.truncate()


def notion_block_to_markdown(block):
    """
    将Notion的block对象转换为Markdown格式。

    参数:
    block (dict): Notion的block对象

    返回:
    str: 转换后的Markdown字符串
    """
    markdown = ""
    block_type = block.get("type")
    if block_type == "paragraph":
        rich_texts = block.get("paragraph", {}).get("rich_text", [])
        for rich_text in rich_texts:
            text = rich_text.get("text")
            link = text.get("link")
            content = text.get("content")
            if link:
                url = link.get("url")
                markdown += f"[{content}]({url})\n"
            else:
                markdown += content + "\n"

    elif block_type == "heading_1":
        rich_texts = block.get("heading_1", {}).get("rich_text", [])
        for rich_text in rich_texts:
            markdown += "# " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "heading_2":
        rich_texts = block.get("heading_2", {}).get("rich_text", [])
        for rich_text in rich_texts:
            markdown += "## " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "heading_3":
        rich_texts = block.get("heading_3", {}).get("rich_text", [])
        for rich_text in rich_texts:
            markdown += "### " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "bulleted_list_item":
        rich_texts = block.get("bulleted_list_item", {}).get("rich_text", [])
        for rich_text in rich_texts:
            markdown += "- " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "numbered_list_item":
        rich_texts = block.get("numbered_list_item", {}).get("rich_text", [])
        for rich_text in rich_texts:
            markdown += "1. " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "to_do":
        rich_texts = block.get("to_do", {}).get("rich_text", [])
        checked = block.get("to_do", {}).get("checked", False)
        for rich_text in rich_texts:
            markdown += "- ["
            markdown += "x" if checked else " "
            markdown += "] " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "quote":
        rich_texts = block.get("quote", {}).get("rich_text", [])
        for rich_text in rich_texts:
            markdown += "> " + rich_text.get("text", {}).get("content", "") + "\n"

    elif block_type == "code":
        language = block.get("code", {}).get("language", "")
        rich_texts = block.get("code", {}).get("rich_text", [])
        markdown += f"```{language}\n"
        for rich_text in rich_texts:
            markdown += rich_text.get("text", {}).get("content", "") + "\n"
        markdown += "```\n"

    return markdown


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
    # print(query_toggl())
    # query_memos()
    # query_run()
    # print(query_memos())
    # print(query_todo())
    # print(query_movie())
