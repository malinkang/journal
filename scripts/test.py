#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, datetime
complete ='▓'
uncomplete ='░'
print(complete)
print(uncomplete)
d0 = datetime(2021, 1, 1)
d1 = datetime(2022, 1, 1)
d3 = datetime.now()
delta = d1 - d0
delta2 = d3 - d0
progress=(delta2.days+5)/delta.days
print(round(progress*20))
result = ""
for i in range(0,round(progress*20)):
    result +=complete
for i in range(0,20-round(progress*20)):
    result +=uncomplete
result = "Year Progress "+result+" "+str(round(progress, 3)*100)+"%"
print(result)