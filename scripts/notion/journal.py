import argparse
from datetime import date, datetime, timedelta
import glob
import os
import time

import pendulum
import notion_api
import util
from utils import ensure_journal_page
from config import (
    DAY_PAGE_ID,
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
        # print(result)
        name = util.get_title(result, "Name")
        day = util.get_formula(result, "倒数日")
        progress = util.get_formula(result, "Progress")
        # print(f"name = {name} day = {day} progress = {progress}")
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
            get_block("bulleted_list_item",rich_text=[get_text(f"今天在多邻国学习了{duration}分钟，完成了{session}单元，共获得{xp}经验")])
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
        url = util.get_url(result, "url")
        urls.append(get_block("embed",url=url))
        # name = util.get_title(result, "Name")
        # text = util.get_rich_text(result, "text")
        # type = util.get_select(result, "Type")
        # if id == None or id == "":
        #     urls.append(f"* {text}")
        # if type == "mastodon":
        #     urls.append("{" + """{{< mastodon status="{id}" >}}""".format(id=id) + "}")
        # else:
        #     urls.append(
        #         "{"
        #         + """{{< tweet user="{name}" id="{id}" >}}""".format(name=name, id=id)
        #         + "}"
        #     )
    return urls


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
        {"property": name, "date": {"before": end}},
    ]
    if len(extras) > 0:
        conditions.extend(extras)
    filter = {"and": conditions}
    return filter


# https://malinkang.notion.site/aaa0f16646be480b8ad31c244f30ed17?v=40fabf9084c442999d02f166eb3e7e2d&pvs=4
def query_movie():
    response = notion_api.query_database(
        database_id="aaa0f16646be480b8ad31c244f30ed17", filter=get_filter(name="日期")
    )
    urls = []
    for result in response.get("results"):
        title = util.get_title(result, "电影名")
        url = util.get_url(result, "豆瓣链接")
        status = result["properties"]["状态"]["status"]["name"]
        rich_text = [
            get_text(status),
            get_text(title,url),
        ]
        urls.append(get_block("bulleted_list_item",rich_text=rich_text))
    return urls


def query_run():
    list = []
    response = notion_api.query_database(
        database_id="8dc2c4145901403ea9c4fb0b10ad3f86", filter=get_filter()
    )
    results = response.get("results")
    for result in results:
        id = util.get_rich_text(result, "id")
        km = results[0]["properties"]["KM"]["formula"]["number"]
        url = f"https://www.strava.com/activities/{id}"
        rich_text=[
            get_text(f"跑步{km}km",url=url)
        ]
        list.append(get_block("bulleted_list_item",rich_text=rich_text))
    return list


# https://www.notion.so/malinkang/736d23cc9ef94bac865cfc9f6393e5d1?v=3a267cd1120649a892e25cc472a255db&pvs=4
def query_mastodon():
    response = notion_api.query_database(
        database_id="736d23cc9ef94bac865cfc9f6393e5d1", filter=get_filter("日期")
    )
    results = response.get("results")
    toots = []
    for result in results:
        properties = result.get("properties")
        title = util.get_title(result, "标题")
        toots.append(get_block("paragraph", rich_text=[get_text(title)]))
        for item in properties.get("资源").get("relation"):
            image = notion_api.client.pages.retrieve(page_id=item.get("id"))
            for file in image.get("properties").get("链接").get("files"):
                file.pop("name")
                toots.append(get_block("image",external=file))
        toots.append(get_block("divider"))
    return toots


def query_book():
    response = notion_api.query_database(
        database_id="25386019c92c81549225d641cc3aae04", filter=get_filter(name="日期")
    )
    books = []
    for result in response.get("results"):
        properties = result.get("properties")
        duration = util.get_number(result, "时长")
        relation = properties.get("书架").get("relation")
        if relation:
            book = notion_api.client.pages.retrieve(
                page_id=properties.get("书架").get("relation")[0].get("id")
            )
            name = util.get_title(book, "书名")
            print(name)
            url = util.get_url(book, "链接")
            rich_text = [
                get_text("读"),
                get_text(f"《{name}》", url),
                get_text(f"{round(duration/60)}分钟"),
            ]
            books.append(get_block("bulleted_list_item", rich_text))
    return books


# https://www.notion.so/malinkang/8db320a226324aa1a20ed7bbc39b7727?v=01e5a358c0f64da19a66dbe220c2ce5f&pvs=4
def query_douban_book():
    books = set()
    response = notion_api.query_database(
        database_id="8db320a226324aa1a20ed7bbc39b7727", filter=get_filter(name="日期")
    )
    for result in response.get("results"):
        title = util.get_title(result, "书名")
        url = util.get_url(result, "豆瓣链接")
        status = result["properties"]["状态"]["status"]["name"]
        books.add(f"[{status}{title}]({url})")
    return books


def query_todo():
    """查询今日完成的任务"""
    results = []
    extras = [{"property": "状态", "status": {"equals": "Done"}}]
    response = notion_api.query_database(
        database_id="14b86019c92c817f8bdedc8f651bb598",
        filter=get_filter(name="完成时间", extras=extras),
    )
    for result in response.get("results"):
        title = result["properties"]["标题"]["title"][0]["text"]["content"]
        url = result.get("public_url")
        rich_text = [get_text(title, url)]
        results.append(get_block("to_do", rich_text, True))
    return results


def get_text(content, url=None):
    text = {
        "type": "text",
        "text": {
            "content": content,
        },
    }
    if url:
        text["text"]["link"] = {"url": url}
    return text


def get_external(url):
    return {"type": "external", "external": {"url": url}}
def get_embed(url):
    return {"type": "embed", "embed": {"url": url}}


def get_block(type, rich_text=None, checked=False,external = None,url=None):
    block = {
        "type": type,
        type: {},
    }
    if rich_text:
        block[type]["rich_text"] = rich_text
    if type == "to_do":
        block[type]["checked"] = checked
    if external:
        block[type] = external
    if url:
        block[type]["url"] = url
    return block


# https://www.notion.so/malinkang/cf6359306f94456da01908af73191a61?v=462ad72e1a4c4c3591a074816dcccbd1&pvs=4
def query_toggl():
    #     # 前天的20点到昨天的8点 搜索睡觉事件
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
    rows = []
    cells = []
    if response.get("results"):
        cells.append([get_text(f"时间")])
        cells.append([get_text(f"分类")])
        cells.append([get_text(f"备注")])
        rows.append(get_table_row(cells))
    for result in response.get("results"):
        start, end = util.get_date(result, "时间")
        emoji = util.get_icon(result)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(start).strftime("%H:%M")
        end = datetime.fromisoformat(end).strftime("%H:%M")
        name = util.get_title(result, "标题")
        note = util.get_rich_text(result, "备注")
        cells = []
        cells.append([get_text(f"{start}-{end}")])
        cells.append([get_text(f"{emoji} {name}")])
        cells.append([get_text(f"{note}")])
        rows.append(get_table_row(cells))
    if rows:

        return get_table(3, rows)


def create():
    response = notion_api.query_database(database_id=DAY_PAGE_ID, filter=get_filter())
    results = response.get("results")
    print(f"查询到{len(results)}条记录")
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
        song = query_music()
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
        # urls = query_bilibili() | query_movie()
        urls = query_bilibili()
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
def get_table_row(cells):
    return {"type": "table_row", "table_row": {"cells": cells}}


def get_table(table_width, children):
    return {
        "type": "table",
        "table": {
            "table_width": table_width,
            "has_column_header": True,
            "has_row_header": False,
            "children": children,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    content = parser.parse_args().content
    date = datetime.now()
    if content:
        date = datetime.strptime(parser.parse_args().content, "%Y-%m-%d")
    page_id = ensure_journal_page(date)
    print(f"创建日记页面 {page_id} 成功")
    if page_id:
        children = []
        song = query_music()
        if song:
            children.append(get_embed(f"https://notion-music.malinkang.com/player?server=notion&type=song&id={song}"))
        todos = query_todo()
        if todos:
            children.append(get_block("heading_2",rich_text=[get_text("✅ ToDo")]))
            children.extend(todos)

        # timelines = query_twitter()
        # if timelines:
        #     children.append(get_block("heading_2",rich_text=[get_text("💬 碎碎念")]))
        #     children.extend(timelines)
        books = query_book()
        if books:
            children.append(get_block("heading_2",rich_text=[get_text("📖 阅读")]))
            children.extend(books)
        duolingo = query_duolingo()
        if duolingo:
            children.append(get_block("heading_2",rich_text=[get_text("📖 学习")]))
            children.extend(duolingo)
        runs = query_run()
        if runs:
            children.append(get_block("heading_2",rich_text=[get_text("❤️ 健康")]))
            children.extend(runs)
        table = query_toggl()
        if table:
            children.append(get_block("heading_2",rich_text=[get_text("⏰ 日程")]))
            children.append(table)
        # movies = query_movie()
        # if movies:
        #     children.append(get_block("heading_2",rich_text=[get_text("📺 电影")]))
        #     children.extend(movies)
        if children:
            print(f"添加 {len(children)} 个块到页面 {page_id}")
            notion_api.client.blocks.children.append(
                block_id=page_id, children=children
            )
    # print(query_movie())
    # # print()
    # print(query_todo())
    # print(query_duoligo())
    # query_twitter()
    # query_run()
    # print(query_memos())
    # print(query_toggl())
    # print(query_movie())
