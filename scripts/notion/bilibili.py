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
    filter = {"property": "Url", "url": {"equals": entry.link}}
    response = notion_api.query_database(database_id=id, filter=filter)
    if(len(response.get("results")) == 0):
        properties = (
            Properties()
            .title(entry.title)
            .select("From","BiliBili")
            .date(start=datetime(*entry.published_parsed[:6]))
            .url("Url", entry.link)
        )
        page = (
            Page()
            .parent(DatabaseParent("de0b737abfd0490abd9e4652073becfe"))
            .cover(unsplash.random())
            .icon("📺")
            .children(Children())
            .properties(properties)
        )
        notion_api.create_page(page)
        print("插入成功")    
   
