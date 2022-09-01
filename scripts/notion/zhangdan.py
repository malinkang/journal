import argparse
import csv
from datetime import datetime
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
import notion_api
import requests
from notion_api import Children


def parse_csv():
    with open('./data/微信支付账单.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_page(row["\ufeff交易时间"],row["交易类型"],row["交易对方"],row["商品"],row["收/支"],float(row["金额(元)"].replace("¥","")),row["备注"])


# 创建Page
def create_page(date,type,payee,product,amount,price,note):
    emo = "💰"
    format_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    cover = "https://64.media.tumblr.com/d08697c9851e4aae0ce26e9d895c9b45/fa0fbfe0c7f3f78f-47/s400x600/d5f378df11819131b2f6fe2239ec201797d4ff97.jpg"
    properties = Properties().title(date).date("日期",date,None).select("交易类型",type).select("交易对方",payee).select("商品",product).select("收/支",amount).number("金额(元)",price).rich_text("备注",note)
    properties = notion_api.get_relation(properties,format_date)
    page  = Page().parent(DatabaseParent("0d52a3d9fda741f78e1af90b30a91a82")).children(Children()).cover(cover).icon(emo).properties(properties)
    notion_api.create_page(page)

headers = {}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("secret")
    parser.add_argument("version")
    options = parser.parse_args()
    headers = {"Authorization": options.secret, "Notion-Version": options.version}
    parse_csv()