#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://developers.notion.com/reference/page#database-parent
class DatebaseParent(dict):
    def __init__(self, database_id):
        self["type"] = "database_id"
        self["database_id"] = database_id
    
