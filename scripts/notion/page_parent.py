#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://developers.notion.com/reference/page#page-parent
class PageParent(dict):
    def __init__(self, page_id):
        self["type"] = "page_id"
        self["page_id"] = page_id
    
