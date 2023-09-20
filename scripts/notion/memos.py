import os
import requests
import json
from datetime import datetime, timezone, timedelta
import pytz
import requests
import mimetypes
# API请求信息
def get_memos():
    url = 'https://memos.malinkang.com/api/v1/memo/all'
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'openId': '65806e0d-dced-483d-8ba4-4ec4d51ccae7'
    }

    # 发送API请求并获取数据
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        json_data = response.text
        data = json.loads(json_data)
        # 设置时区为Asia/Shanghai
        tz = pytz.timezone('Asia/Shanghai')
        # 获取今天的日期
        now = datetime.now(tz) - timedelta(days=2)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timedelta(days=1)
        
        # 过滤数据
        filtered_data = []
        for item in data:
            created_ts = datetime.fromtimestamp(item["createdTs"], tz)
            print(created_ts)
            if today_start <= created_ts < tomorrow_start:
                filtered_data.append(item)
        
        # 处理过滤后的数据
        for item in filtered_data:
            id = item["id"]
            content = item["content"]
            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")
            dir = f"content/posts/{year}/{year}-{month}-{day}/memos/{id}"
            if(not os.path.exists(dir)):
                os.makedirs(dir)

            if(len(item["resourceList"]) > 0):
                content += "\n"
                content += f'{{{{< gallery match="memos/{id}/images/*" sortOrder="desc" rowHeight="150" margins="5" thumbnailResizeOptions="600x600 q90 Lanczos" showExif=true previewType="blur" embedPreview=true loadJQuery=true >}}}}'
                images_dir = f"content/posts/{year}/{year}-{month}-{day}/memos/{id}/images"
                if(not os.path.exists(images_dir)):
                    os.makedirs(images_dir)
                for resource in item["resourceList"]:
                    id = resource.get("id")
                    extension = mimetypes.guess_extension(resource.get("type"))
                    file = f"{images_dir}/{id}{extension}"
                    url = f"https://memos.malinkang.com/o/r/{id}"
                    print(extension)
                    download(url,file)
            with open(f"{dir}/memos.md", "w") as f:
                f.write(content)
    else:
        print(f"请求失败，状态码：{response.status_code}")





# 文件的URL
def download(url,file):
    if(os.path.exists(file)):
        print(f"文件已存在 {file}")
        return
    # 发送HEAD请求获取响应头信息
    response = requests.head(url)

    if response.status_code == 200:
        # 发送GET请求获取文件内容
        response = requests.get(url)

        if response.status_code == 200:
            # 保存文件到本地
            with open(file, 'wb') as f:
                f.write(response.content)
            print(f"文件已保存为 {file}")
        else:
            print(f"无法下载文件，状态码：{response.status_code}")
    else:
        print(f"无法获取响应头信息，状态码：{response.status_code}")



if __name__ == "__main__":
    get_memos()