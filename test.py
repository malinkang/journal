from datetime import datetime, timedelta, timezone

now = datetime.now()
# print(now)
print(now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
# date = now - timedelta(hours=1)
# print((now - date ).seconds)