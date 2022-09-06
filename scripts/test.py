



from datetime import datetime
import re
import feedparser
import json


if __name__ == "__main__":
    pattern = r'想看|看过|想读|听过|想读|读过|玩过|在读'
    r = re.match(pattern,'想读小黄人大眼萌：神偷奶爸前传')
    if r:
        print(r.group(0))
    # d = feedparser.parse("https://www.douban.com/feed/people/malinkang/interests")
    # print(d)
    # create_page(options.id)
    # test = {'object': 'list', 'results': [{'object': 'page', 'id': 'bf7e75bb-9920-4fb5-a194-d0d4269a92c0', 'created_time': '2022-07-12T05:18:00.000Z', 'last_edited_time': '2022-07-12T05:18:00.000Z', 'created_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'last_edited_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '53514517-87d9-403f-b48d-9a9c20f31f43'}, 'archived': False, 'properties': {'date': {'id': '%3EORN'}, 'id': {'id': 'a%5D%3EN'}, 'url': {'id': 'eGey'}, 'image': {'id': 'f%3C%7CS'}, 'text': {'id': '~Yd%5D'}, 'Name': {'id': 'title'}}, 'url': 'https://www.notion.so/malinkang-bf7e75bb99204fb5a194d0d4269a92c0'}, {'object': 'page', 'id': 'fdbf8eae-911a-4fde-84e9-1bb2779074a9', 'created_time': '2022-07-12T04:13:00.000Z', 'last_edited_time': '2022-07-12T04:13:00.000Z', 'created_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'last_edited_by': {'object': 'user', 'id': 'f7a343af-85b4-4bf5-a307-29ac21a849ce'}, 'cover': None, 'icon': None, 'parent': {'type': 'database_id', 'database_id': '53514517-87d9-403f-b48d-9a9c20f31f43'}, 'archived': False, 'properties': {'date': {'id': '%3EORN'}, 'id': {'id': 'a%5D%3EN'}, 'url': {'id': 'eGey'}, 'image': {'id': 'f%3C%7CS'}, 'text': {'id': '~Yd%5D'}, 'Name': {'id': 'title'}}, 'url': 'https://www.notion.so/malinkang-fdbf8eae911a4fde84e91bb2779074a9'}], 'next_cursor': None, 'has_more': False, 'type': 'page', 'page': {}}
    # print(json.dumps(test))
    # test = {"haha":"哈哈哈"}
    # print('haha' in test)
    # tup1 = (1, 2, 3)
    # print(tup1[0])
    # date = datetime.now()
    # date = []
    # print(isinstance(date, list))
    # test = {'object': 'page', 'id': 'd7421bf0-3d82-4378-86fc-7927bd974fa9', 'created_time': '2022-07-13T03:32:00.000Z', 'last_edited_time': '2022-07-13T03:34:00.000Z', 'created_by': {'object': 'user', 'id': '569ac58e-5ffa-4471-8988-944ddf0eae5e'}, 'last_edited_by': {'object': 'user', 'id': '569ac58e-5ffa-4471-8988-944ddf0eae5e'}, 'cover': {'type': 'external', 'external': {'url': 'https://images.unsplash.com/photo-1657247882823-955a21e2f18a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNjEzMDZ8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NTc2ODMxNTU&ixlib=rb-1.2.1&q=80&w=400'}}, 'icon': {'type': 'emoji', 'emoji': '✅'}, 'parent': {'type': 'database_id', 'database_id': '97955f34-653b-4658-bc0a-aa50423be45f'}, 'archived': False, 'properties': {'Status': {'id': '3E6J'}, 'Date Created': {'id': 'DrOp'}, 'Duration': {'id': 'EetM'}, 'Assign': {'id': 'F%24%23%5D'}, 'Tag': {'id': 'LV%3B%3C'}, 'Category': {'id': 'f%60Fh'}, 'Priority': {'id': "rqJ'"}, 'Date': {'id': 'z.OF'}, '🍅番茄钟': {'id': '%7DJHE'}, '🍅': {'id': '~kRu'}, 'Name': {'id': 'title'}}, 'url': 'https://www.notion.so/hugo-d7421bf03d82437886fc7927bd974fa9'}
    # print(json.dumps(test))
