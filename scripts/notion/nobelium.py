import argparse
from email import contentmanager
from pydoc import pager

import notion_api
import dateutils
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties


def create():
    title = dateutils.format_date_with_week()
    filter = {"property":"Name","rich_text":{"equals":title}}
    response = notion_api.query_database("294060cd-e13e-4c29-b0ac-6ee490c8a448",filter)
    cover = response.get("results")[0].get("cover").get("external").get("url")
    icon = response.get("results")[0].get("icon").get("emoij")
    name=notion_api.get_title(response,"Name")
    content = ""
    weather=notion_api.get_rich_text(response,"天气")
    if(weather is not None):
        content += "今天天气"+weather
    aq=notion_api.get_rich_text(response,"空气质量")
    if(weather is not None):
        content += "，空气质量"+aq
    highest=notion_api.get_rich_text(response,"最高温度")
    if(highest is not None):
        content += "，最高温度"+highest
    lowest=notion_api.get_rich_text(response,"最低温度")
    if(lowest is not None):
        content += "，最低温度"+lowest
    if(content==""):
        pass
    else:
        content+="。"
    children=Children().add_block("paragraph",content)
    properties = Properties().title(name)
    page = Page().parent(DatabaseParent("48107861338540dc97f6985be1e2a198")).properties(properties=properties).children(children).cover(cover).icon(icon)
    notion_api.create_page(page=page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    create()