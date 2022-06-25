## 脚本执行

```shell
python3 scripts/create_diary.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '294060cd-e13e-4c29-b0ac-6ee490c8a448' '2021-08-16' 'b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb'

python3 scripts/notion/create_diary.py '294060cd-e13e-4c29-b0ac-6ee490c8a448' 'b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb'

python3 scripts/test.py  '294060cd-e13e-4c29-b0ac-6ee490c8a448'

python3 scripts/github.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13' '20211101'
python3 scripts/blog.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13'

python3 scripts/write_diary.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'

python3 scripts/telegram.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13' '20211108'

python3 scripts/secretary.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-05-13' '20211101'
python3 scripts/cover.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16' 'b0cbd23d5d1b188ffbf313d0c78071280f3d506d0279a1d31302ad87548b1beb'

python3 scripts/notion/sleep.py '{"start":"22\/6\/22周三 上午12:00","end":"22\/6\/22周三 上午8:14","duration":"8.17"}'

python3 scripts/toggl.py 'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'

python3 scripts/notion/weather.py '{"lowest":"21°C","aqi":"40","highest":"38°C","weather":"大部晴朗"}'
  
```

### 跑步

```shell
python3 scripts/keep.py  18611145755  KFitness@4  'Bearer secret_xvMkQzLkCRtZL478L8MhvLdIDOxicjjSUm9U9voAwbb' '2021-08-16'
```

## TODO

- [ ] 睡眠计入Time tacker中，更新前先检查是否已经记录过
- [ ] 写日记自动从计划database中获取任务名称建立TODO List
- [ ] 每天更新计划是否完成

## 文档

* [钉钉](//https://developers.dingtalk.com/document/app/custom-robot-access/title-jfe-yo9-jl2)