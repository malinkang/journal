#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
from datetime import datetime, timedelta
import requests
import notion_api
from notion_api import Properties
from notion_api import Children
from notion_api import DatabaseParent
from notion_api import Page
import unsplash


def sync():
    sorts = [{"property": "Date", "direction": "descending"}]
    page_size = 1
    response = notion_api.query_database(
        "d8eee75d8c1049e7aa3dd6614907bb04", sorts=sorts, page_size=page_size
    )
    end = notion_api.get_date(response, "Date").get("end")
    print(end)
    auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")
    params = {"start_date": end}
    response = requests.get(
        "https://api.track.toggl.com/api/v8/time_entries", params=params, auth=auth
    )
    print("hhhh = "+response.text)
    for task in response.json():
        if task.get("pid") is not None and task.get("stop") is not None:
            newTags = []
            tags = task.get("tags")
            if tags is not None:
                for tag in tags:
                    newTag = {"name": tag}
                    newTags.append(newTag)
            start = datetime.fromisoformat(task.get("start"))
            start = start +timedelta(hours=8)
            end =datetime.fromisoformat(task.get("stop"))
            end = end+timedelta(hours=8)
            response = requests.get(
                "https://api.track.toggl.com/api/v8/projects/" + str(task.get("pid")),
                auth=auth,
            )
            print(response.json())
            data = response.json().get("data")
            project = data.get("name")
            cid = data.get("cid")
            response = requests.get(
                "https://api.track.toggl.com/api/v8/clients/" + str(cid),
                auth=auth,
            )
            print(response.json())
            client = response.json().get("data").get("name")
            description = ""
            if task.get("description") is not None:
                description = task.get("description")
            properties = (
                Properties()
                .title("时间统计")
                .date(start=start, end=end)
                .select("二级分类", project)
                .select("一级分类", client)
                .rich_text("备注", description)
            )

            properties = notion_api.get_relation(properties, datetime.now())
            page = Page().parent(DatabaseParent("d8eee75d8c1049e7aa3dd6614907bb04")).children(Children()).properties(properties).cover(unsplash.random()).icon("⏰")
            notion_api.create_page(page)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    sync()
