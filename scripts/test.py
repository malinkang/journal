#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime,timedelta


print(datetime.now())

time = datetime(2022, 1, 1, 0, 0)

print(time-datetime.now())

yestoday = datetime.now()-timedelta(days=1)

print(yestoday)


print(yestoday < datetime.now())


now = datetime.now()

#获取今日0点
zero = datetime(now.year,now.month,now.day,0,0)
print(zero < datetime.now())