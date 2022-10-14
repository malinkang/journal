from datetime import datetime
from notion_api import Properties
from notion_api import DatabaseParent
from notion_api import Page
from notion_api import Children
import notion_api
import unsplash
TODO = "97955f34653b4658bc0aaa50423be45f"

def add_todo(title):
    properties = (
        Properties()
        .title(title)
        .date()
        .select("Status", "Not Started")
        .select("Priority", "High 🔥")
        .people("Assign", ["6d411501-82d6-46e5-b809-97c0fdce722c"])
    )
    parent = DatabaseParent(TODO)
    page = (
        Page()
        .parent(parent)
        .children(Children())
        .cover(unsplash.random())
        .icon("✅")
        .properties(properties)
    )
    response = notion_api.create_page(page=page)
    return response.get("id")

if __name__ == "__main__":
    now = datetime.now()
    print(now.day)
    print(now.weekday())
    if(now.weekday() < 5):
        add_todo("订餐")