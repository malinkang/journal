#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import unsplash
import notion
import dateutils
from datetime import datetime, timedelta
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
from notion_api import Children
import notion_api


# 创建Page
def create_page():
    emo = "☀️"
    tomorrow = datetime.now() + timedelta(days=1)
    week = tomorrow.strftime("第%V周")
    month = tomorrow.strftime("%-m月")
    title = dateutils.format_date_with_week(date=tomorrow)
    cover = unsplash.random()
    tags = [week,month]
    properties = Properties().title(title).date(start=tomorrow).multi_select("Tag",tags)
    properties = notion_api.get_relation(properties,tomorrow,False)
    parent = DatabaseParent("294060cd-e13e-4c29-b0ac-6ee490c8a448")
    page  = Page().parent(parent).children(Children()).cover(cover).icon(emo).properties(properties)
    notion_api.create_page(page=page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    create_page()
