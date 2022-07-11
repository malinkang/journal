#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta, timezone


def format_utc(time):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    date = date.replace(microsecond=0)
    return date

def get_date(time):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    date = date.replace(microsecond=0).astimezone(tz=timezone(timedelta(hours=8)))
    date = timedelta(hours=8) + date
    return date