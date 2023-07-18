from datetime import datetime

# 要转换的字符串
date_string = "2023-07-06T11:27:50Z"

# 转换为 datetime 对象
datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")

print("转换后的 datetime 对象:", datetime_object.strftime("%m"))