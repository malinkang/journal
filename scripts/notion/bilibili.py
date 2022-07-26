from datetime import datetime
import json
import feedparser
import notion_api
from notion_api import Page
from notion_api import Properties
from notion_api import Children
from notion_api import DatabaseParent
import unsplash

d = feedparser.parse("https://rsshub.app/bilibili/user/coin/27440979")
id = "de0b737abfd0490abd9e4652073becfe"
for entry in d.entries:
    filter = {"property": "id", "rich_text": {"equals": entry.id}}
    response = notion_api.query_database(id, filter)
    print(len(response.get("results")))
    if(len(response.get("results")) == 0):
        properties = (
            Properties()
            .title(entry.title)
            .date(start=datetime(*entry.published_parsed[:6]))
            .rich_text("id", entry.id)
            .rich_text("link", entry.link)
        )
        page = (
            Page()
            .parent(DatabaseParent("de0b737abfd0490abd9e4652073becfe"))
            .cover(unsplash.random())
            .icon("💰")
            .children(Children())
            .properties(properties)
        )
        notion_api.create_page(page)
        print("插入成功")    
   
