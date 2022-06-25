
from notion_client import Client
from pprint import pprint

client = Client(auth="secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb")
def create_page(page):
    response = client.pages.create(parent=page["parent"],properties=page["properties"],children =page["children"],icon = page["icon"],cover = page["cover"])
    pprint(response)

def update_page(page_id,page):
    response = client.pages.update(page_id,properties=page["properties"],icon=page["icon"])
    pprint(response)

def query_database(database_id,filter):
    response = client.databases.query(database_id=database_id,filter=filter)
    pprint(response)
    return response
