"""Utility helpers for creating or retrieving journal pages in Notion."""

from datetime import datetime
from typing import Optional

import dateutils
from notion_api import Page, Children, DatabaseParent, Properties
import notion_api
import unsplash

JOURNAL_DATABASE_ID = "48107861338540dc97f6985be1e2a198"
EMOJI_ICON = "☀️"


def _build_default_properties(page_date, title, slug) -> Properties:
    year = page_date.strftime("%Y")
    month = page_date.strftime("%-m月")
    week = page_date.strftime("第%V周")
    return (
        Properties()
        .title(title)
        .date(property="date", start=page_date)
        .multi_select("tags", [year, month, week])
        .rich_text("slug", slug)
        .select("type", "Post")
        .select("status", "Published")
    )


def create_journal_page(
    page_date,
    title,
    slug,
    properties: Optional[Properties] = None,
    icon: Optional[str] = None,
):
    """Create a journal page and return the full Notion response."""
    cover = unsplash.random()

    base_properties = _build_default_properties(page_date, title, slug)

    if properties:
        base_properties.update(properties)

    parent = DatabaseParent(JOURNAL_DATABASE_ID)
    icon_value = icon or EMOJI_ICON
    page = (
        Page()
        .parent(parent)
        .children(Children())
        .cover(cover)
        .icon(icon_value)
        .properties(base_properties)
    )
    return notion_api.create_page(page=page)



def ensure_journal_page(
    page_date: Optional[datetime] = None,
    properties: Optional[Properties] = None,
    icon: Optional[str] = EMOJI_ICON,
):
    """Return existing page id for the given date (defaults to now).

    When `properties` is provided the fields are merged into the defaults before
    page creation. The `icon` emoji defaults to `☀️` but can be overridden. If a
    matching page already exists and both `properties` and `icon` are truthy, the
    page is updated with the merged properties and new icon.
    """
    if page_date is None:
        page_date = datetime.now()
    title = dateutils.format_date_with_week(date=page_date)
    slug = page_date.strftime("%Y-%m-%d")

    filter = {"property": "title", "title": {"equals": title}}

    response = notion_api.client.databases.query(
        database_id=JOURNAL_DATABASE_ID, filter=filter
    )
    results = response.get("results", [])

    if results:
        page_id = results[0].get("id")
        for duplicate in results[1:]:
            notion_api.client.blocks.delete(duplicate.get("id"))
        if properties and icon:
            merged_properties = _build_default_properties(page_date, title, slug)
            merged_properties.update(properties)
            notion_api.update_page_with_icon(
                page_id,
                merged_properties,
                {"type": "emoji", "emoji": icon},
            )
        return page_id

    page = create_journal_page(
        page_date,
        title,
        slug,
        properties=properties,
        icon=icon,
    )
    if page and page.get("id"):
        return page.get("id")
    return None
