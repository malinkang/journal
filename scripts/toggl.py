#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
from datetime import datetime, timedelta, timezone
import requests
import notion


def sync():
    body = {
        "sorts": [{"property": "时间", "direction": "descending"}],
        "page_size":1
    }
    r = requests.post(
        "https://api.notion.com/v1/databases/d8eee75d8c1049e7aa3dd6614907bb04/query",
        headers=headers,
        json=body,
    )
    start = r.json().get("results")[0].get("properties").get("时间").get("date").get("end")
    print(start)
    auth = ("2ef95512ce5b1528809f9a03a68e02b1", "api_token")
    params = {"start_date": start}
    response = requests.get(
        "https://api.track.toggl.com/api/v8/time_entries", params=params, auth=auth
    )
    for task in response.json():
        if task.get("pid") is not None and task.get("stop") is not None:
            newTags = []
            tags = task.get("tags")
            if tags is not None:
                for tag in tags:
                    newTag = {"name": tag}
                    newTags.append(newTag)
            start = datetime.strptime(
                task.get("start"), "%Y-%m-%dT%H:%M:%S%z"
            ).astimezone(tz=timezone(timedelta(hours=8)))
            start = start.replace(microsecond=0).isoformat()
            end = datetime.strptime(task.get("stop"), "%Y-%m-%dT%H:%M:%S%z").astimezone(
                tz=timezone(timedelta(hours=8))
            )
            end = end.replace(microsecond=0).isoformat()
            response = requests.get(
                "https://api.track.toggl.com/api/v8/projects/" + str(task.get("pid")),
                auth=auth,
            )

            data = response.json().get("data")
            project = data.get("name")
            cid = data.get("cid")
            response = requests.get(
                "https://api.track.toggl.com/api/v8/clients/" + str(cid),
                auth=auth,
            )
            client = response.json().get("data").get("name")
    

            description = ""
            if task.get("description") is not None:
                description = task.get("description")
            properties = {
                "title": notion.get_title("时间统计"),
                "时间": {"date": {"start": start, "end": end}},
                "二级分类": {"select": {"name": project}},
                "一级分类": {"select": {"name": client}},
                "备注": {
                    "rich_text": [{"type": "text", "text": {"content": description}}]
                },
            }
            properties = notion.get_relation(properties, datetime.now())
            body = {
                "parent": {
                    "type": "database_id",
                    "database_id": "d8eee75d8c1049e7aa3dd6614907bb04",
                },
                "properties": properties,
                "cover": notion.get_cover(),
                "icon": {"type": "emoji", "emoji": "⏰"},
            }
            requests.post(
                "https://api.notion.com/v1/pages/", headers=headers, json=body
            )


headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    options = parser.parse_args()
    headers = {"Authorization": options.secret, "Notion-Version": options.version}
    sync()
