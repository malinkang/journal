#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, datetime,timedelta


print(datetime.now())

time = datetime(2022, 1, 1, 0, 0)

print(time-datetime.now())

yestoday = datetime.now()-timedelta(days=1)

tomorrow = datetime.now()+timedelta(days=1)

print(yestoday)

print(tomorrow)

week_day_dict = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}


print(datetime.strftime(tomorrow,'%Y年%m月%d 星期'+week_day_dict[tomorrow.weekday()]))
print(tomorrow.weekday())


print(yestoday < datetime.now())


now = datetime.now()

#获取今日0点
zero = datetime(now.year,now.month,now.day,0,0)
print(zero < datetime.now())

