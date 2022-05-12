# -*- coding: utf-8 -*-
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

timestamp = str(round(time.time() * 1000))
secret = 'SEC2f9be8006cc5e536be490464e7a70f1e33dbe52f17b037da05dfe3e4b3de6e43'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
print(timestamp)
print(sign)
url = 'https://oapi.dingtalk.com/robot/send?access_token=6a9469ea7489bb8af087103912134701f0f9d9463b87afacae4d40096bb9893c&timestamp='+timestamp+'&sign='+sign
headers = {'Content-Type': 'application/json; charset=utf-8'}
body = {"msgtype":"text","text":{"content":"应用名称：BBooster\n修改内容：修改新手保护\n版本号：1.0.0\n下载地址：https://pgyer.com/bbooster"},"at":{"atMobiles":["18611145755","18701552797"]},"isAtAll":True}
r = requests.post(url,headers=headers,data=json.dumps(body))
print(r.json())