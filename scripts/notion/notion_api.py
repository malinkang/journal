
import json
from urllib import response
from notion_client import Client
from page import Page
from pprint import pprint

client = Client(auth="secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb")
def create_page(page):
    response = client.pages.create(parent=page["parent"],properties=page["properties"],children =page["children"],icon = page["icon"],cover = page["cover"])
    pprint(response)
