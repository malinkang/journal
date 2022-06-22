from datetime import datetime, timedelta, timezone
print(datetime.now())
# print(datetime.now().strftime("%y/%-m/%d"))
d = "22/6/22周三 下午12:00"
date = d[:d.find("周")]+" "+d[d.find("午")+1:]
print(date)
if "上午" in d:
    date = datetime.strptime(date,"%y/%m/%d %I:%M")
else :
    date = datetime.strptime(date,"%y/%m/%d %H:%M")
print(date)