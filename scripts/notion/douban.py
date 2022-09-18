from calendar import month
from cmath import pi
from datetime import date, datetime
import csv
from nis import match
from os import stat
import re
import time
import feedparser
import notion_api
from notion_api import Page
from notion_api import Properties
from notion_api import Children
from notion_api import DatabaseParent
from bs4 import BeautifulSoup
import requests


url = 'https://www.douban.com/feed/people/malinkang/interests'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

MOVIE_DATABASE_ID = "f551b7e002ac4b0ab73eb34d0dd53951"
BOOK_DATABASE_ID = "c7efdba75f4146ad84a3f5b773998859"
rating_dict = {
    '很差': '⭐️',
    '较差': '⭐️⭐️',
    '还行': '⭐️⭐️⭐️',
    '推荐': '⭐️⭐️⭐️⭐️',
    '力荐': '⭐️⭐️⭐️⭐️⭐️',
}
rating_dict2 = {
    '': '⭐️',
    '1': '⭐️',
    '2': '⭐️⭐️',
    '3': '⭐️⭐️⭐️',
    '4': '⭐️⭐️⭐️⭐️',
    '5': '⭐️⭐️⭐️⭐️⭐️',
}

def feed_parser():
    d = feedparser.parse(url)
    for entry in d.entries:
        title = entry['title']
        pattern = r'想看|在看|看过|想读|最近在读|读过'
        status = ""
        m = re.match(pattern, title)
        if m:
            status = m.group(0)
            if(status == '最近在读'):
                status = status[2:]
        link = entry['link']
        rating = ''
        note = ''
        date = datetime(*entry.published_parsed[:6])
        soup = BeautifulSoup(entry['description'])
        
        for p in soup.find_all('p'):
            if '推荐: ' in p.string:
                rating = rating_dict[p.string.split(": ")[1]]
            if '备注: ' in p.string:
                note = p.string.split(": ")[1]
        if ('看' in status):
            parse_movie(date, rating, note, status, link)
        elif ('读' in status):
            print(title)
            parse_book(date, rating, note, status, link)

def parse_movie_csv():
    with open('./data/db-movie-20220918.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['\ufeff标题']
            print(title)
            status='看过'
            date = datetime.strptime(row['打分日期'],'%Y/%M/%d')
            rating = rating_dict2[row['个人评分']]
            note = row['我的短评']
            link =row['条目链接']
            time.sleep(1)
            parse_movie(date, rating, note, status, link)

def parse_movie(date, rating, note, status, link):
    f = {"property": "条目链接", "url": {"equals": link}}
    response = notion_api.query_database(
        database_id=MOVIE_DATABASE_ID, filter=f)
    if (len(response['results']) > 0):
        update(date, rating, note, status,response['results'][0]['id'])
        return
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content)
    title = soup.find(property='v:itemreviewed').string
    year = soup.find('span', {'class': 'year'}).string[1:-1]
    info = soup.find(id='info')
    # print('info ',info)
    cover = soup.find(id='mainpic').img['src']
    # 导演
    directors = list(filter(lambda x: '/' not in x,info.find('span', {'class': 'attrs'}).strings))
    # 演员
    actors = list()
    actor_span=info.find(
        'span', {'class': 'actor'})
    if actor_span!=None:
        actors = list(map(lambda x: x.string,actor_span.find_all('a')))
    # 类型
    genre = list(map(lambda x: x.string, info.find_all(property='v:genre')))
    country = ''
    imdb = ''
    for span in info.find_all('span', {'class': 'pl'}):
        if ('制片国家/地区:' == span.string):
            country = span.next_sibling.string
        if ('IMDb:' == span.string):
            imdb = 'https://www.imdb.com/title/'+span.next_sibling.string.strip()

    insert_movie(title, date, link, cover, rating, note, status,
                 year, directors, actors, genre, country, imdb)


def parse_book(date, rating, note, status, link):
    f = {"property": "条目链接", "url": {"equals": link}}
    response = notion_api.query_database(
        database_id=BOOK_DATABASE_ID, filter=f)
    if (len(response['results']) > 0):
        update(date, rating, note, status,response['results'][0]['id'])
        return
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content)
    title = soup.find(property='v:itemreviewed').string
    #
    info = soup.find(id='info')
    info = list(map(lambda x: x.replace(':', ''), list(
        filter(lambda x: '\n' not in x, info.strings))))
    dict = {}
    for i in range(0, len(info), 2):
        dict[info[i].strip()] = info[i+1]

    cover = soup.find(id='mainpic').img['src']
    insert_book(title, date, link, cover, dict, rating, note, status)

def update(date,rating,note, status,page_id):
    properties = (
        Properties()
        .date(property='打分日期', start=date)
        .select('状态', status)
    )
    if rating != "":
        properties.select("个人评分", rating)
    if note != "":
        properties.rich_text("我的短评", note)
    notion_api.update_page(page_id=page_id,properties=properties)
def insert_movie(title, date, link, cover, rating, note, status, year, directors, actors, genre, country, imdb):
    properties = (
        Properties()
        .title(title)
        .date(property='打分日期', start=date)
        .file("海报", cover)
        .url("条目链接", link)
        .number('上映年份', int(year))
        .select('状态', status)
        .multi_select('导演', directors)
        .multi_select('主演', actors[0:10])
        .multi_select('类型', genre)
        .rich_text('制片国家', country)
       
    )
    if imdb!="":
         properties.url("IMDb 链接", imdb)
    if rating != "":
        properties.select("个人评分", rating)
    if note != "":
        properties.rich_text("我的短评", note)
    page = (
        Page()
        .parent(DatabaseParent(MOVIE_DATABASE_ID))
        .cover(cover)
        .icon("🎬")
        .children(Children())
        .properties(properties)
    )
    notion_api.create_page(page)
    print("插入成功")


def insert_book(title, date, link, cover, info, rating, note, status):
    l = list(map(int, info['出版年'].split('-')))
    l.append(1)
    properties = (
        Properties()
        .title(title)
        .date(property='打分日期', start=date)
        .file("海报", cover)
        .url("条目链接", link)
        .date(property='出版日期', start=datetime(*l))
        .rich_text('作者', info['作者'])
        .number('ISBN', int(info['ISBN']))
        .rich_text('出版社', info['出版社'])
        .select('状态', status)
    )
    if rating != "":
        properties.select("个人评分", rating)
    if note != "":
        properties.select("我的短评", note)

    page = (
        Page()
        .parent(DatabaseParent(BOOK_DATABASE_ID))
        .cover(cover)
        .icon("📚")
        .children(Children())
        .properties(properties)
    )
    notion_api.create_page(page)
    print("插入成功")


if __name__ == "__main__":
    # feed_parser()
    parse_movie_csv()
