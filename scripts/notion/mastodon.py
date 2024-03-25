
from datetime import datetime, timedelta
import feedparser
import notion_api
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
from notion_api import Children
import unsplash

urls = [
    "https://rsshub.app/mastodon/acct/malinkang@mastodon.social/statuses",
    # "https://rsshub.app/twitter/user/Carve_Time",
]
for url in urls:
    d = feedparser.parse(url)
    print(d)
    for entry in d.entries:
        id = entry.link.split("/")[-1]
        name = entry.link.split("/")[-3]
        filter = {"property": "id", "rich_text": {"equals": id}}
        response = notion_api.query_database(database_id="5351451787d9403fb48d9a9c20f31f43", filter=filter)
        if(len(response.get("results")) == 0):
            date = datetime.strptime(entry['published'],'%a, %d %b %Y %H:%M:%S %Z')+timedelta(hours=8)
            properties = (
                Properties()
                .title(name)
                .date(start=date)
                .rich_text("text", entry.title)
                .rich_text("id", id)
                .select("Type","mastodon")
                .url("url", entry.link)
            )
            page = (
                Page()
                .parent(DatabaseParent("5351451787d9403fb48d9a9c20f31f43"))
                .cover(unsplash.random())
                .icon("🐦")
                .children(Children())
                .properties(properties)
            )
            notion_api.create_page(page)
