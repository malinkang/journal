import argparse
import csv
from datetime import datetime
import json
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
import notion_api
import requests
from notion_api import Children



# 创建Page
def create_page(content):
    content = json.loads(content)
    purchase_time = content['purchase_time']
    product_name = content['product_name']
    product_price = content['product_price']
    merchant = content['merchant']
    payment_method = content['payment_method']
    product_category = content['product_category']
    emo = "💰"
    format_date = datetime.fromisoformat(purchase_time)
    cover = "https://64.media.tumblr.com/d08697c9851e4aae0ce26e9d895c9b45/fa0fbfe0c7f3f78f-47/s400x600/d5f378df11819131b2f6fe2239ec201797d4ff97.jpg"
    properties = Properties().title("账单").date(property="日期",start=format_date,end=None,time_zone=None).select("支付方式",payment_method).select("商家",merchant).select("商品",product_name).select("分类",product_category).number("金额(元)",product_price)
    properties = notion_api.get_relation(properties,format_date)
    page  = Page().parent(DatabaseParent("0d52a3d9fda741f78e1af90b30a91a82")).children(Children()).cover(cover).icon(emo).properties(properties)
    notion_api.create_page(page)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    create_page(options.content)