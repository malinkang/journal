#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, datetime
import json
import requests
import argparse
import time 
#获取封面

def getDatebase(accessKey):
    r = requests.post("https://api.notion.com/v1/databases/48fa2b28ce294476b12046589ac33663/query",headers=headers)
    results = r.json().get("results")
    for result in results:
        if result.get("cover") is None:
            cover = getCover(accessKey,2)
            print("cover "+cover)
            emoji = "🤖"
            body = {
            "cover": {"type": "external", "external": {"url": cover}},
            "icon": {"type": "emoji", "emoji": emoji}
        }
            r = requests.patch("https://api.notion.com/v1/pages/"+result.get("id"),headers=headers,json=body)
            print(r.json())

def getCover(accessKey,count):
    params = {"client_id": accessKey, "orientation": "landscape","count":count}
    r = requests.get('https://api.unsplash.com/photos/random', params=params)
    print(r.text)
    cover = r.json().get("urls").get("small")
    return cover
headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    parser.add_argument("accessKey")
    options = parser.parse_args()
    headers = {'Authorization': options.secret, "Notion-Version": options.version}
    getDatebase(options.accessKey)