# -*- coding: utf-8 -*-
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

response = requests.get("https://v1.jinrishici.com/all.json")
content = response.json().get("content")+"\n"
content += "小伙子们该点餐了。\n"
content += "点餐地址：https://meican.com/"
timestamp = str(round(time.time() * 1000))
secret = 'SECbedf1c1ae59913385480be658b9542035b918765b5db3fbb6f935cbef28c79c0'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
url = 'https://oapi.dingtalk.com/robot/send?access_token=3ae55a3b30fcafdf4e75ab01b416f5963e4be01cf405ad13e28ff480b569c50b&timestamp='+timestamp+'&sign='+sign
headers = {'Content-Type': 'application/json; charset=utf-8'}
print(content)
body = {"msgtype":"text","text":{"content":content},"at":{"atMobiles":["13201697002","18611145755","13126675216"]},"isAtAll":True}
r = requests.post(url,headers=headers,data=json.dumps(body))
print(r.json())