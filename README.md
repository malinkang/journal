## 脚本执行

```shell
python3 scripts/create_diary.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '294060cd-e13e-4c29-b0ac-6ee490c8a448' '2021-08-16' 'b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb'

python3 scripts/notion/create_diary.py '294060cd-e13e-4c29-b0ac-6ee490c8a448' 'b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb'

python3 scripts/test.py  '294060cd-e13e-4c29-b0ac-6ee490c8a448'

python3 scripts/notion/hugo.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13' '20211101'
python3 scripts/blog.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13'

python3 scripts/write_diary.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'
python3 scripts/notion/weight.py '{"weight":"20"}'

python3 scripts/telegram.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13' '20211108'

python3 scripts/secretary.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13' '20211101'
python3 scripts/cover.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16' 'b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb'

python3 scripts/notion/sleep.py '{"start":"22\/6\/22周三 上午12:00","end":"22\/6\/22周三 上午8:14","duration":"8.17"}'

python3 scripts/toggl.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'
python3 scripts/notion/read.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'

python3 scripts/notion/weather.py '{"lowest":"21°C","aqi":"40","highest":"38°C","weather":"大部晴朗"}'
  
python3 scripts/zhangdan.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13'
```

### 跑步

```shell
python3 scripts/notion/keep.py  18611145755  KFitness@4  'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'
python3 -m github_poster weread --weread_cookie 'RK=KZ0Ew/JFS7; ptcz=cba8e45558c5cab1cccb43896ab8d5980c5506b676460d857e0bf24492a9479f; wr_gid=223315174; wr_fp=2017239275; ptui_loginuin=458832194; pgv_info=ssid=s1778422266; pgv_pvid=5013319515; wr_vid=16308016; wr_pf=0; wr_rt=web@MQH3cqXN3ib5l5f0~ol_WL; wr_localvid=79c322606f8d73079ce03da; wr_name=CarveTime; wr_avatar=https://res.weread.qq.com/wravatar/WV0016-RnaEL_g5XKTnGxtCRB5EW76/0; wr_gender=1; wr_skey=iRnMYrvT' --year 2021-2022 --me "malinkang"

python3 scripts/notion/weread.py 'RK=KZ0Ew/JFS7; ptcz=cba8e45558c5cab1cccb43896ab8d5980c5506b676460d857e0bf24492a9479f; wr_gid=223315174; wr_vid=16308016; wr_skey=JwIRK8YS; wr_pf=0; wr_rt=web@tYV~PulLBf27nZ3~LrZ_WL; wr_localvid=79c322606f8d73079ce03da; wr_name=CarveTime; wr_avatar=https://res.weread.qq.com/wravatar/WV0016-RnaEL_g5XKTnGxtCRB5EW76/0; wr_gender=1; _pk_ref.4.5084=["","",1665573770,"https://x.weread.qq.com/"]; _pk_id.4.5084=1aa918092ac19997.1665573770.; _pk_ses.4.5084=1; wr_vid=16308016; wr_skey=vTZxhvYM; wr_auth={"cpIds":[],"cpEBook":0,"cpLecture":0,"cpAdmin":0,"cpAdminPublisher":false,"cpAdminBalance":false}'
```

python3 -m github_poster forest --forest_email linkang.ma@gmail.com --forest_password FFitness06 --year 2023 --cn

## TODO

## 文档

* [钉钉](//https://developers.dingtalk.com/document/app/custom-robot-access/title-jfe-yo9-jl2)


```
//1676472
curl -u linkang.ma@gmail.com:TFitness@5 \
  -H "Content-Type: application/json" \
  -X GET   https://api.track.toggl.com/api/v9/workspaces



curl -u 2ef95512ce5b1528809f9a03a68e02b1:api_token \
  -H "Content-Type: application/json" \
  -X GET  https://api.track.toggl.com/api/v9/me/projects

```

python3 scripts/notion/weread.py 'RK=KZ0Ew/JFS7; ptcz=cba8e45558c5cab1cccb43896ab8d5980c5506b676460d857e0bf24492a9479f; wr_gid=223315174; wr_fp=2017239275; ptui_loginuin=458832194; pgv_info=ssid=s1778422266; pgv_pvid=5013319515; wr_vid=16308016; wr_pf=0; wr_rt=web@MQH3cqXN3ib5l5f0~ol_WL; wr_localvid=79c322606f8d73079ce03da; wr_name=CarveTime; wr_avatar=https://res.weread.qq.com/wravatar/WV0016-RnaEL_g5XKTnGxtCRB5EW76/0; wr_gender=1; wr_skey=iRnMYrvT'


python3 scripts/notion/douban.py 'RK=KZ0Ew/JFS7; ptcz=cba8e45558c5cab1cccb43896ab8d5980c5506b676460d857e0bf24492a9479f; wr_gid=223315174; wr_fp=2017239275; ptui_loginuin=458832194; pgv_info=ssid=s1778422266; pgv_pvid=5013319515; wr_vid=16308016; wr_pf=0; wr_rt=web@MQH3cqXN3ib5l5f0~ol_WL; wr_localvid=79c322606f8d73079ce03da; wr_name=CarveTime; wr_avatar=https://res.weread.qq.com/wravatar/WV0016-RnaEL_g5XKTnGxtCRB5EW76/0; wr_gender=1; wr_skey=iRnMYrvT'


https://neodb.social/oauth/authorize/?response_type=code&client_id=tXFd1sDShGbVS1nRhBWPbE9gFguFbg5QGp4cs2X3&redirect_uri=https://blog.malinkang.com

curl -X POST https://neodb.social/oauth/token/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "client_id=tXFd1sDShGbVS1nRhBWPbE9gFguFbg5QGp4cs2X3" \
-d "client_secret=kyt99Ft7jnHqq41li49jgjBdrPG6LFMTDCQPoN71dCKexO0eOZ6tXuAc96evWcOn6lnkYtbz5FbK80a9dngLcNb4Qd8Ca2P5PBVQtRJvb4GptXQHyjvvu70Tq83ePKCt" \
-d "code=6RaJ8jWp2Qdk2KRnvDDgbWnpF96rd9" \ 
-d "redirect_uri=https://blog.malinkang.com" \
-d "grant_type=authorization_code"

curl -X POST 'https://api.notion.com/v1/databases/294060cde13e4c29b0ac6ee490c8a448/query' \
  -H 'Authorization: Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' \
  -H 'Notion-Version: 2022-06-28' \
  -H "Content-Type: application/json"


curl -X POST 'https://api.notion.com/v1/databases/294060cde13e4c29b0ac6ee490c8a448/query' \
-H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
-H 'Notion-Version: 2022-06-28' \
-H "Content-Type: application/json" \
--data '{
"filter": {
  "or": [
    {
      "property": "In stock",
"checkbox": {
"equals": true
}
    },
    {
"property": "Cost of next trip",
"number": {
"greater_than_or_equal_to": 2
}
}
]
},
"sorts": [
  {
    "property": "Last ordered",
    "direction": "ascending"
  }
]
}'

zne2VZVg3ren893HtBLkPkByed5pYe

curl -X POST https://neodb.social/oauth/token/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "client_id=tXFd1sDShGbVS1nRhBWPbE9gFguFbg5QGp4cs2X3" \
-d "client_secret=kyt99Ft7jnHqq41li49jgjBdrPG6LFMTDCQPoN71dCKexO0eOZ6tXuAc96evWcOn6lnkYtbz5FbK80a9dngLcNb4Qd8Ca2P5PBVQtRJvb4GptXQHyjvvu70Tq83ePKCt" \
-d "code=zne2VZVg3ren893HtBLkPkByed5pYe" \
-d "redirect_uri=https://blog.malinkang.com" \
-d "grant_type=authorization_code"