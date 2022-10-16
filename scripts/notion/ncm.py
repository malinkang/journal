from datetime import datetime, timedelta
import feedparser
import notion_api
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
from notion_api import Children
import unsplash


d = feedparser.parse("https://rsshub.app/ncm/playlist/7648872348")
for entry in d.entries:
    filter = {"property": "id", "rich_text": {"equals": entry.id}}
    response = notion_api.query_database("46beb49d60b84317a0a2c36a0a024c71", filter)
    print(len(response.get("results")))
    if(len(response.get("results")) == 0):
        date = datetime.strptime(entry['published'],'%a, %d %b %Y %H:%M:%S %Z')+timedelta(hours=8)
        properties = (
            Properties()
            .title(entry.title)
            .date(start=date)
            .rich_text("id", entry.id)
            .rich_text("link", entry.link)
        )
        page = (
            Page()
            .parent(DatabaseParent("46beb49d60b84317a0a2c36a0a024c71"))
            .cover(unsplash.random())
            .icon("💰")
            .children(Children())
            .properties(properties)
        )
        notion_api.create_page(page)
        print("插入成功")   