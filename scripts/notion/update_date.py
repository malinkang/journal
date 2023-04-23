# 更新年
import notion_api
from config import (
    BILL_DATABASE_ID,
    BOOK_DATABASE_ID,
    MOVIE_DATABASE_ID,
    WEREAD_DATABASE_ID,
)
from util import get_date
from util import get_title
from notion_api import get_relation
from notion_api import Properties
from datetime import datetime

dict = {
    # BILL_DATABASE_ID:"日期",
    # BOOK_DATABASE_ID:"打分日期",
    # MOVIE_DATABASE_ID:"打分日期",
    WEREAD_DATABASE_ID: "Date",
}


def query_year(id, name):
    filter = {
        "and": [
            {"property": "Year", "relation": {"is_empty": True}},
            {"property": name, "date": {"is_not_empty": True}},
        ]
    }
    response = notion_api.query_database(id, filter)
    for result in response["results"]:
        date = datetime.fromisoformat(get_date(result, name))
        properties = get_relation(Properties(), date)
        notion_api.update_page(result["id"], properties)


if __name__ == "__main__":
    for key, value in dict.items():
        query_year(key, value)
