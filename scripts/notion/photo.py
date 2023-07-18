import argparse
import glob
import hashlib
import json
import os
import requests

def download_image(url,file_name, save_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            ext = content_type.split('/')[-1] if content_type else 'jpg'
            filename = f"{file_name}.{ext}"
            save_path = os.path.join(save_dir, filename)

            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("图片下载成功！保存路径：", save_path)
        else:
            print("图片下载失败，状态码：", response.status_code)
    except Exception as e:
        print("图片下载出现异常：", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    dict = json.loads(options.content)
    date = dict.get("mediaMetadata").get("creationTime").split("T")[0].split("-")
    base_url = dict["baseUrl"]
    file_name = hashlib.sha256(base_url.encode()).hexdigest()
    dir = f"./content/posts/{date[0]}/{date[0]}-{date[1]}-{date[2]}/images"
    if(not os.path.exists(dir)):
        os.makedirs(dir)
    files = glob.glob(f"{dir}/{file_name}.*")
    if len(files) == 0:
        download_image(dict['baseUrl'],file_name,dir)
    else:
        print("图片已存在")