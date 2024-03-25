#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import json
import requests
import argparse
import dateutils
import notion_api
from datetime import datetime
from notion_api import Properties
from notion_api import Page

#搜索笔记
def search(content):
    title = dateutils.format_date_with_week()
    filter = {"property":"Name","rich_text":{"equals":title}}
    response = notion_api.query_database(database_id="294060cd-e13e-4c29-b0ac-6ee490c8a448",filter=filter)
    if(len([response["results"]])>0):
        id = response["results"][0].get("id")
        update(id,content)
    


def update(id, content):
    content = json.loads(content)
    location = content['location']
    properties=Properties().rich_text("位置",location)
    notion_api.update_page(id,properties)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    search(options.content)
