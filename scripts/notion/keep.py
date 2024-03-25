#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import json
import math
import notion
import time
import requests
from datetime import datetime, timedelta, timezone
import unsplash
from notion_api import Properties
from notion_api import Page
import notion_api
from notion_api import DatabaseParent
from notion_api import Children
import stravalib
from stravalib import unithelper
from config import (
    KEEP_DATABASE_ID
)
LOGIN_API = "https://api.gotokeep.com/v1.1/users/login"
RUN_DATA_API = "https://api.gotokeep.com/pd/v3/stats/detail?dateUnit=all&type=running&lastDate={last_date}"
RUN_LOG_API = "https://api.gotokeep.com/pd/v3/runninglog/{run_id}"
client = stravalib.Client()


def login():
    client_id = "67037"
    client_secret = "9ea364fa0db767d52770b3a3deaf0f5e1ceafb51"
    refresh_token = "6145d313d69e93ba801fd6754ad1363157f72972"
    response= client.refresh_access_token(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
    )   
    print(response)
    get_activities()
  


def get_activities():
    now = datetime.now()
    today = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    tommorrow = today + timedelta(days=1)
    filters = {"before":tommorrow, "after":today}
    print(filters)
    activities = client.get_activities(**filters)
    for activity in activities:
        if(activity.type == "Run"):
            print(activity)
            print(activity.id)
            print(activity.athlete)
            print(activity.type)
            print(activity.start_date)
            print(activity.start_date_local)
            print(activity.distance.num)
            print(activity.moving_time)
            print(activity.elapsed_time)
            print(activity.timezone)
            print(activity.location_city)
            id = str(activity.id)
            # break
            if not exists(id):
                add_to_notion(activity)
            else:
                print("已存在")


def is_today(record):
    today = datetime.now().strftime("%-m月%d日")
    return today == record.get("date")

# 检查是否存在
def exists(id):
    time.sleep(0.3)
    filter = {"property": "id", "rich_text": {"equals": id}}
    response = notion_api.query_database(database_id=KEEP_DATABASE_ID, filter=filter)
    return len(response.get("results")) > 0



def add_to_notion(activity):
    time.sleep(0.3)
    title  =datetime.strftime(activity.start_date_local, "%-m月%d日")
    # cover = unsplash.random()
    date = activity.start_date_local
    properties = Properties().title(title).date(
        start=date).number("距离", activity.distance.num).rich_text("id", str(activity.id))
    notion_api.get_relation(properties, date)
    page = Page().parent(DatabaseParent(KEEP_DATABASE_ID)).children(
        Children()).cover(cover="https://images.unsplash.com/photo-1693817027569-908462a0bca1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2ODUwfDB8MXxyYW5kb218fHx8fHx8fHwxNjk1MDkyNTI3fA&ixlib=rb-4.0.3&q=80&w=4800").icon("🏃🏻").properties(properties)
    r = notion_api.create_page(page=page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    login()
