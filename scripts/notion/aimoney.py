import argparse
import csv
from datetime import datetime
import json
from notion_api import Properties
from notion_api import Page
from notion_api import DatabaseParent
import notion_api
from notion_api import Children


def parse_csv(content):
    content = json.loads(content)
    create_page(content.get("date"),"商户消费",content.get("merchant"),content.get("name"),"支出",content.get("cost"),content.get("method"))

#https://www.notion.so/malinkang/8bdadd5592534cc79586d29e86756bcd?v=61dba9e443b246b6bfd71f2dbac1f5f9&pvs=4

# https://www.notion.so/malinkang/e8390b5ff8a34789b0c4703cc6615afc?v=e121672b6a1647dfb794b2a9f8f5406a&pvs=4
def query_card(name,id):
    cover = "https://64.media.tumblr.com/d08697c9851e4aae0ce26e9d895c9b45/fa0fbfe0c7f3f78f-47/s400x600/d5f378df11819131b2f6fe2239ec201797d4ff97.jpg"
    filter = {"property": "Name", "title": {"equals": name}}
    response = notion_api.query_database(id,filter)
    if(len(response.get("results")) == 0):
        properties = Properties().title(name)
        page  = Page().parent(DatabaseParent(id)).children(Children()).cover(cover).icon("💳").properties(properties)
        return notion_api.create_page(page).get("id")
    else:
        return response.get("results")[0].get("id")
#https://www.notion.so/malinkang/dd39319e45964a64899ae5371c0a6421?v=03688e8572364e66b5929e934ec2f973&pvs=4    

#https://www.notion.so/malinkang/f4d2374344ca409aa22d40e8d33833eb?v=c1f12cf999c84d7f8a528dae0c9872d7&pvs=4

#https://www.notion.so/malinkang/194f66886cd8479899d38b0fb0b7da26?v=00f4a1e51b1848bd975a377dfca44335&pvs=4
def query():
    filter = {"property":"Name","title":{"does_not_contain":"年"}}
    response = notion_api.query_database("194f66886cd8479899d38b0fb0b7da26",filter)
    dict = {}
    print(len(response.get("results")))
    for result in response.get("results"):
        d = result.get("id")
        n = result.get("properties").get("Name").get("title")[0].get("plain_text")
        if(len(result.get("properties").get("Year").get("relation"))>0):
            id = result.get("properties").get("Year").get("relation")[0].get("id")
            # print("\n-----------------------------------\n")
            # print(n)
            if id not in dict:
                name = query_year(id)
                dict[id] = name
            name = dict[id]
            properties = Properties().title(f'{name}年{n}')
            notion_api.update_page(d,properties)


def query_year(id):
   print(id)
   return notion_api.retreve_a_page(id).get("properties").get("Name").get("title")[0].get("plain_text")
    
# 创建Page
def create_page(date,type,payee,product,amount,price,note,method):
    emo = "💰"
    payee = query_card(payee,"e8390b5ff8a34789b0c4703cc6615afc")
    method = query_card(method,"8bdadd5592534cc79586d29e86756bcd")
    format_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    cover = "https://64.media.tumblr.com/d08697c9851e4aae0ce26e9d895c9b45/fa0fbfe0c7f3f78f-47/s400x600/d5f378df11819131b2f6fe2239ec201797d4ff97.jpg"
    properties = Properties().date("日期",date,None).select("交易类型",type).relation("商家",payee).relation("支付方式",method).title(product).select("收/支",amount).number("金额(元)",price).rich_text("备注",note)
    properties = notion_api.get_relation(properties,format_date)
    page  = Page().parent(DatabaseParent("0d52a3d9fda741f78e1af90b30a91a82")).children(Children()).cover(cover).icon(emo).properties(properties)
    notion_api.create_page(page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    parse_csv(options.content)
