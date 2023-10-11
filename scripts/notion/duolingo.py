

import argparse
from datetime import datetime
import pendulum

import requests
from notion_api import Properties
from notion_api import DatabaseParent
from notion_api import Children
from notion_api import Page
from util import get_title
import unsplash
import notion_api

headers = {
    "Accept": "*/*",
    "User-Agent": "request",
}

#https://www.notion.so/malinkang/82277d8180564a949728b594faf4fd87?v=c8b9c4569eb146128681a8ea476e38cc&pvs=4

def get_weekly_reading():
    """
    获取周阅读数据
    """
    headers["Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjoyOTk3NTA4M30.X3RwmIAOT9MFwpgMztMHtgLliVbcXvvgJXuj3qROU_g"
    r = requests.get("https://ios-api-2.duolingo.com/2017-06-30/users/29975083/xp_summaries?endDate=2023-10-11&startDate=2023-10-11&timezone=Asia/Shanghai",headers=headers)
    if r.ok:
        summaries = r.json()["summaries"]
        for item in summaries:
            date = str(item.get("date"))
            gainedXp = item.get("gainedXp")
            page_id = query_read_times(date)
            if(page_id!=""):
                update_read_time(page_id,gainedXp)
            else:
                insert_read_times(date,gainedXp,datetime.fromtimestamp(int(date)) )

def insert_read_times(title,  xp, date):
    properties = (
        Properties()
        .title(title)
        .number("Xp", xp)
        .date(start=date.strftime("%Y-%m-%dT00:00:00"))
    )
    properties = notion_api.get_relation(properties, date=date)
    page = (
        Page()
        .parent(DatabaseParent("82277d8180564a949728b594faf4fd87"))
        .children(Children())
        .properties(properties)
        .cover(unsplash.random())
        .icon("🇺🇸")
    )
    notion_api.create_page(page)

def update_read_time(id, xp):
    properties = (
        Properties()
        .number("Xp", xp)
    )
    notion_api.update_page(id, properties)


def query_read_times(timestamp):
    filter = {
        "and": [
            {"property": "Timestamp", "title": {"equals": timestamp}},
        ]
    }
    id = ""
    response = notion_api.query_database(
        "82277d8180564a949728b594faf4fd87", filter)
    results = response["results"]
    if len(results) > 0:
        id = results[0]["id"]
    return id
def make_month_list():
    start = pendulum.datetime(2022, 1, 1)
    end = pendulum.datetime(2023, 12, 31)
    period = pendulum.period(start, end)
    month_list = list(period.range("months"))
    # filter
    month_list = [m for m in month_list if m < pendulum.now()]
    return month_list
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    get_weekly_reading()
    # for m in make_month_list():
    #     print(m.end_of("month").to_date_string())
    #     print(m.to_date_string())