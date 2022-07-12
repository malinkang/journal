import argparse
from datetime import datetime
import notion_api
import dateutils
from notion_api import Page
from notion_api import Children, DatabaseParent
from notion_api import Properties

today = datetime.now().strftime("%Y-%m-%d")


def query_day():
    response = notion_api.query_database("d34e3250832a4b5fb44054a8b364df2a")
    list = []
    for index in range(0, len(response.get("results"))):
        name = notion_api.get_title(response, "Name", index)
        day = notion_api.get_formula_string(response, "倒数日", index)
        progress = notion_api.get_formula_string(response, "Progress", index)
        list.append(name + day + " " + progress)
        # notion_api.get_rich_text(response, "倒数日")
    return list


def query_twitter():
    filter = {"property": "date", "date": {"equals": today}}
    response = notion_api.query_database("5351451787d9403fb48d9a9c20f31f43", filter)
    urls = []
    for index in range(0, len(response.get("results"))):
        url = notion_api.get_rich_text(response, "image", index)
        urls.append(url)
    return urls


def query_weight():
    filter = {"property": "Date", "date": {"equals": today}}
    response = notion_api.query_database("34c0db4313b24c3fac8e25436f5b3530", filter)
    if len(response.get("results")) > 0:
        return notion_api.get_number(response, "体重")
    return 0


def query_book():
    filter = {"property": "Date", "date": {"equals": today}}
    response = notion_api.query_database("cca71ece15ac48a68c34e5f86a2e6b38", filter)
    if len(response.get("results")) > 0:
        name = notion_api.get_title(response, "Name")
        start = notion_api.get_number(response, "Start")
        end = notion_api.get_number(response, "End")
        return "读《" + name + "》" + str(start) + "-" + str(end) + "》" + name
    return None


def query_todo():
    filter = {"property": "Date", "date": {"equals": today}}
    response = notion_api.query_database("97955f34653b4658bc0aaa50423be45f", filter)
    todo_list = []
    if len(response.get("results")) > 0:
        todo_list.append(notion_api.get_title(response, "Name"))
    return todo_list


def query_toggl():
    filter = {"property": "Date", "date": {"equals": today}}
    response = notion_api.query_database("d8eee75d8c1049e7aa3dd6614907bb04", filter)
    toggl_list = []
    for index in range(0, len(response.get("results"))):
        date = notion_api.get_date(response, "Date", index)
        # 格式化一下只保留时间
        start = datetime.fromisoformat(date.get("start")).strftime("%H:%M")
        end = datetime.fromisoformat(date.get("end")).strftime("%H:%M")
        name = notion_api.get_select(response, "二级分类", index)
        note = notion_api.get_rich_text(response, "备注", index)
        result = start + "-" + end + "：" + name
        if note is not None and note is not "":
            result += "，" + note
        toggl_list.append(result)
    return toggl_list


def create():
    title = dateutils.format_date_with_week()
    slug = datetime.now().strftime("%Y-%m-%d")
    filter = {"property": "Name", "rich_text": {"equals": title}}
    response = notion_api.query_database("294060cd-e13e-4c29-b0ac-6ee490c8a448", filter)
    cover = response.get("results")[0].get("cover").get("external").get("url")
    icon = response.get("results")[0].get("icon").get("emoji")
    name = notion_api.get_title(response, "Name")
    content = ""
    weather = notion_api.get_rich_text(response, "天气")
    tag = notion_api.get_multi_select(response, "Tag")
    print(tag)
    if weather is not None:
        content += "今天天气" + weather
    aq = notion_api.get_number(response, "空气质量")
    if weather is not None:
        content += "，空气质量" + str(aq)
    highest = notion_api.get_rich_text(response, "最高温度")
    if highest is not None:
        content += "，最高温度" + highest
    lowest = notion_api.get_rich_text(response, "最低温度")
    if lowest is not None:
        content += "，最低温度" + lowest
    if content == "":
        pass
    else:
        content += "。"
    location = notion_api.get_rich_text(response, "位置")
    children = Children().add_block("paragraph", content)

    days = query_day()
    if len(days) > 0:
        children.add_block("heading_2", "📅 倒数日")
        for day in days:
            children.add_block("bulleted_list_item", day)

    children.add_block("heading_2", "✅ ToDo")
    book = query_book()
    if book is not None:
        children.add_block("to_do", book)
    todos = query_todo()
    for todo in todos:
        children.add_block("to_do", todo)

    children.add_block("heading_2", "❤️ 健康")
    weight = query_weight()
    if weight is not None:
        children.add_block("bulleted_list_item", "体重：" + str(weight) + "斤")

    children.add_block("heading_2", "⏰ 时间统计")
    toggls = query_toggl()
    for toggl in toggls:
        children.add_block("bulleted_list_item", toggl)

    urls = query_twitter()
    if len(urls) > 0:
        children.add_block("heading_2", "💬 碎碎念")
        for url in urls:
            children.add_embed_block(url)
    properties = (
        Properties()
        .title(name)
        .rich_text("slug", slug)
        .select("status", "Published")
        .select("type", "Post")
        .date("date")
    )
    if location is not None:
        properties.rich_text("summary", location)
    items = []
    for item in tag:
        items.append(item.get("name"))
    properties.multi_select("tags", items)
    page = (
        Page()
        .parent(DatabaseParent("48107861338540dc97f6985be1e2a198"))
        .properties(properties=properties)
        .children(children)
        .cover(cover)
        .icon(icon)
    )
    notion_api.create_page(page=page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    options = parser.parse_args()
    create()
    # query_toggl()
    # print(query_todo())
    # query_day()
    # # query_twitter()
    # query_weight()
    # # print(query_weight())
    # query_book()
