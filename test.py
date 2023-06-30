import requests

url = "http://test.upgrade-admin.ptc.sg2.api/v1/release/upload"

payload = {'req': '{"productName":"Product 1","packageName":"com.example.app_8","channel":"channel1","versionCode":"1.0.0","versionName":"Release 1.0","updateLog":"Some update log","md5":"8d9599818a0a232e00708c034cff9762","developWaInfo":{"versionCode":"2.0.0","versionName":"Release 2.0","md5":"def456","releaseTime":1667952000000,"expireTime":1699488000000},"configWaInfo":{"versionCode":"3.0.0","versionName":"Release 3.0","md5":"ghi789","releaseTime":1667952000000,"expireTime":1699488000000}}'}
files=[
  ('file',('README',open('README.md','rb'),'application/octet-stream'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
