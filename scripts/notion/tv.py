import datetime
import json
import logging
import time
import requests
from notion_client import Client


def get_tv_shows():
    # 设置Trakt API的请求头
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'Authorization': 'Bearer 1439bef323df01acd75f46dc1331341148b89ac17ca0d207e1cdf3f8f68b3a1c',
        'trakt-api-key': '5e4c7346bf29ef6e75975f6c08496ce504bac3927a5923dc5083085ae99becaa'
    }
    # 设置请求URL和参数
    url = 'https://api.trakt.tv/users/me/history'
    params = {
        'type': 'shows',  # 获取剧集
        'limit': 10  # 设置每页返回的记录数量
    }
    # 发送GET请求
    shows = []
    response = requests.get(url, headers=headers, params=params)
    # 解析响应JSON数据
    if response.status_code == 200:
        shows.extend(response.json())
    else:
        print('请求失败：', response.status_code)
    return shows

def get_trakt_token(code):
    """
    根据Trakt的code获取token
    """
    url = "https://api.trakt.tv/oauth/token"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "code": code,
        "client_id": "5e4c7346bf29ef6e75975f6c08496ce504bac3927a5923dc5083085ae99becaa",
        "client_secret": "624f50edc6dc1367fef336b51190cbf3a4258e1fe74d4264180ee0fc59df3239",  # 请替换为实际的client_secret
        "redirect_uri": "https://malinkang.com",
        "grant_type": "authorization_code"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        logging.error(f"获取token失败，状态码: {response.status_code}")
        return None


def query(imdb):
    """检查是否已经插入过 如果已经插入了就删除"""
    print(imdb)
    time.sleep(0.3)
    filter = {
        "property": "IMDb 链接",
        "url": {
            "equals": f"https://www.imdb.com/title/{imdb}"
        }
    }
    response = client.databases.query(
        database_id="f551b7e002ac4b0ab73eb34d0dd53951", filter=filter)
    return response["results"]


def check_if_exists(id):
    time.sleep(0.3)
    print(id)
    filter = {
        "property": "ID",
        "rich_text": {
            "equals": id
        }
    }
    response = client.databases.query(
        database_id="301da784bddd41b692ee711e08150487", filter=filter)
    return len(response["results"]) > 0


def insert_to_notion(title, id, date, season, number, imdb, url, page_id,cover):
    parent = {
        "database_id": "301da784bddd41b692ee711e08150487",
        "type": "database_id"
    }
    properties = {
        "Name": {"title": [{"type": "text", "text": {"content": title}}]},
        "ID": {"rich_text": [{"type": "text", "text": {"content": id}}]},
        "IMDB": {"rich_text": [{"type": "text", "text": {"content": imdb}}]},
        "🎥 电影": {"relation": [{"id": page_id}]},
        "Date": {"date": {"start": date.strftime("%Y-%m-%d %H:%M:%S"),"time_zone": "Asia/Shanghai"} },
        "URL": {"url": url},
        "Season": {"number": season},
        "Number": {"number": number},
    }
    icon = {
        "type": "external",
        "external": {
            "url": cover
        }
    }
    client.pages.create(parent=parent,icon=icon, properties=properties)


if __name__ == '__main__':
    notion_token = "secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb"
    client = Client(
        auth=notion_token,
        log_level=logging.DEBUG
    )
    code = "your_code_here"  # 假设这是获取的code
    # shows = get_trakt_token("070f977cf78935d64c7f61fa3c7719c7792636e63396ad965bcb2ddbf0e578db")
    shows = get_tv_shows()
    # 将tv shows写入到shows.json中
    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(shows, f, ensure_ascii=False, indent=4)
    # for show in shows:
    #     id = str(show.get("id"))
    #     if check_if_exists(id):
    #         continue

    #     imdb = show.get("show").get("ids").get("imdb")
    #     results = query(imdb)
    #     if len(results) > 0:
    #         date = datetime.datetime.strptime(
    #             show.get("watched_at"), "%Y-%m-%dT%H:%M:%S.%fZ")+datetime.timedelta(hours=8)
    #         season = show.get("episode").get("season")
    #         number = show.get("episode").get("number")
    #         title = results[0].get("properties").get("标题").get("title")[
    #             0].get("text").get("content")
    #         url = results[0].get("properties").get("条目链接").get("url")
    #         print(results[0].get("properties").get("海报"))
    #         cover = results[0].get("properties").get("海报").get("files")[0].get("external").get("url")
    #         insert_to_notion(title, id, date, season, number,
    #                          imdb, url, results[0].get("id"),cover)
