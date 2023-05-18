import datetime
import logging
import time
import requests
from notion_client import Client


def get_tv_shows():
    # 设置Trakt API的请求头
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'Authorization': 'Bearer c99d5256b5483f3067febc4fdf47f950e76f9732a4c35cb0492ffa5bebc16633',
        'trakt-api-key': '31c70c1d138849b946bf2497fe099f87dc7dd800a771a3755f9485f0bb69b5ea'
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
    shows = get_tv_shows()
    for show in shows:
        id = str(show.get("id"))
        if check_if_exists(id):
            continue

        imdb = show.get("show").get("ids").get("imdb")
        results = query(imdb)
        if len(results) > 0:
            date = datetime.datetime.strptime(
                show.get("watched_at"), "%Y-%m-%dT%H:%M:%S.%fZ")+datetime.timedelta(hours=8)
            season = show.get("episode").get("season")
            number = show.get("episode").get("number")
            title = results[0].get("properties").get("标题").get("title")[
                0].get("text").get("content")
            url = results[0].get("properties").get("条目链接").get("url")
            print(results[0].get("properties").get("海报"))
            cover = results[0].get("properties").get("海报").get("files")[0].get("external").get("url")
            insert_to_notion(title, id, date, season, number,
                             imdb, url, results[0].get("id"),cover)
