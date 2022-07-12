#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import notion
import requests
from datetime import date, datetime, timedelta, timezone
import unsplash
from notion_api import Properties
from notion_api import Page
import notion_api
from notion_api import DatabaseParent
from notion_api import Children
LOGIN_API = "https://api.gotokeep.com/v1.1/users/login"
RUN_DATA_API = "https://api.gotokeep.com/pd/v3/stats/detail?dateUnit=all&type=running&lastDate={last_date}"
RUN_LOG_API = "https://api.gotokeep.com/pd/v3/runninglog/{run_id}"



def login( mobile, passowrd):
    data = {"mobile": mobile, "password": passowrd}
    r = requests.post(LOGIN_API, headers=keep_headers, data=data)
    if r.ok:
        token = r.json()["data"]["token"]
        keep_headers["Authorization"] = f"Bearer {token}"
        get_run_id()

def get_run_id():
    last_date=0
    r = requests.get(RUN_DATA_API.format(last_date=last_date), headers=keep_headers)
    if r.ok:
        last_date = r.json()["data"]["lastTimestamp"]
        print(last_date)
        for record in filter(is_today,r.json().get("data").get("records")):
            for log in record.get("logs"):
                id = log.get("stats").get("id")
                get_run_data(id,record.get("date"))


def is_today(record):
    today = (datetime.now()-timedelta(days=1)).strftime("%-m月%d日")
    return today == record.get("date")
               
def get_run_data(id,title):
    r = requests.get(RUN_LOG_API.format(run_id=id), headers=keep_headers)
    if r.ok:
        data = r.json().get("data")
        print(data)
        start = datetime.fromtimestamp(data.get("startTime")/1000)
        end = datetime.fromtimestamp(data.get("endTime")/1000)
        cover = data.get("polylineSnapshot")
        if cover is None:
            cover = unsplash.random()
        distance = round(float(data.get("distance"))/1000,2)
        
        add_to_notion(start,end,cover,distance,title)
def add_to_notion(start,end,cover,distance,title,):
    date = start
    start = start.replace(microsecond=0)
    end = end.replace(microsecond=0)
    properties = Properties().title(title).date(start = start,end=end).number("距离",distance)
    notion_api.get_relation(properties,date)
    page = Page().parent(DatabaseParent("8dc2c4145901403ea9c4fb0b10ad3f86")).children(Children()).cover(cover).icon("🏃🏻").properties(properties)
    r = notion_api.create_page(page=page)


keep_headers  = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phone_number")
    parser.add_argument("password")
    options = parser.parse_args()
    login(options.phone_number, options.password) 