
from datetime import datetime, timedelta
import feedparser
import notion_api
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
from notion_api import Children
import unsplash

urls = [
    "https://rsshub.malinkang.com/twitter/user/malinkang"
    # "https://rsshub.malinkang.com/twitter/user/malinkang/readable=1&authorNameBold=1&showAuthorInTitle=1&showAuthorInDesc=1&showQuotedAuthorAvatarInDesc=1&showAuthorAvatarInDesc=1&showEmojiForRetweetAndReply=1&showRetweetTextInTitle=0&addLinkForPics=1&showTimestampInDescription=1&showQuotedInTitle=1&heightOfPics=150"
    # "https://rsshub.app/twitter/user/malinkang/readable=1&authorNameBold=1&showAuthorInTitle=1&showAuthorInDesc=1&showQuotedAuthorAvatarInDesc=1&showAuthorAvatarInDesc=1&showEmojiForRetweetAndReply=1&showRetweetTextInTitle=0&addLinkForPics=1&showTimestampInDescription=1&showQuotedInTitle=1&heightOfPics=150",
    # "https://rsshub.app/twitter/user/Carve_Time/readable=1&authorNameBold=1&showAuthorInTitle=1&showAuthorInDesc=1&showQuotedAuthorAvatarInDesc=1&showAuthorAvatarInDesc=1&showEmojiForRetweetAndReply=1&showRetweetTextInTitle=0&addLinkForPics=1&showTimestampInDescription=1&showQuotedInTitle=1&heightOfPics=150",
]
for url in urls:
    d = feedparser.parse(url)
    print(d)
    for entry in d.entries:
        id = entry.link.split("/")[-1]
        name = entry.link.split("/")[-3]
        filter = {"property": "id", "rich_text": {"equals": id}}
        response = notion_api.query_database(database_id="5351451787d9403fb48d9a9c20f31f43",filter=filter)
        if(len(response.get("results")) == 0):
            date = datetime.strptime(entry['published'],'%a, %d %b %Y %H:%M:%S %Z')+timedelta(hours=8)
            properties = (
                Properties()
                .title(name)
                .date(start=date)
                .rich_text("text", entry.title)
                .rich_text("id", id)
                .url("url", entry.link)
                .select("Type","Twitter")
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
