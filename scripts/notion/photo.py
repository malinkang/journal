import argparse
import os
import requests

# def download_image(url, save_dir):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             content_type = response.headers.get('content-type')
#             ext = content_type.split('/')[-1] if content_type else 'jpg'
#             filename = f"image.{ext}"
#             save_path = os.path.join(save_dir, filename)

#             with open(save_path, 'wb') as f:
#                 f.write(response.content)
#             print("图片下载成功！保存路径：", save_path)
#         else:
#             print("图片下载失败，状态码：", response.status_code)
#     except Exception as e:
#         print("图片下载出现异常：", e)

# # 示例：下载图片
# image_url = "https://lh3.googleusercontent.com/lr/AJUiC1yl2httNN3wgSk671rK9yNrpzQT8EkH0ihS4yNrlLPUnNSWC5pM3mhF_I1qO1mCbvtgNne80H2UkmOetwKiWEqJqeuG4zQHefiONlcVhU3cPdvPdd5FGOrK1BawnH_2OVJ8dMx25WG9in_tb82FIB9jdnDp8FNj5b1RYJpliNm72T076QqI3r4TMA5fhvjo4fQ33AxMGEjPl5VVDH3QH7nS5XiQ8oZ075fYDGHJH3F8lSKgqHSAaT2QP6JiB0MtN09SCsFhVgW2TmG_O9e--I0zvMwUsBMrf3fMGO02ILGCgWtWdWWCloRbo2n5saTTpKS7JtJNPS3ZH8UGrl4rhpt34VhdL8Kc57lrdnaXf7Y6sWBGc-bOZYKmz73ZhFdOOvAAFgwm-DNzTnS9g10KT7RnRzgAUBQhkBzSe5VOWHx-gMpNRd4c_VX_RzAZS9eNzVUHIR2-72O2tjCpQ_hgDp12dvh7NhGaSozBcepzU77bSyne5lFXrTAXsN-IVZQ7jjRRnAAAcPW9wIGzgrPDLlv90sVGhdRAcFXzxAXPOXUZflRhf6a8_4SC7oDusg1wiLCREhP-V1WCLRd2o8f7eQzC5LO5hth42UPX_7KUFg7GJEKzpah61mKmNTP_sdrARo76fneldF7qxf6DpiBXB01Mkj1c_YMDTrePIZs9Wgu4PVg82mjFx9cJi8nPVFcVCtKI7vBnxNm0J-tdSFNekeRsm_LI14jTqc5BiXKW7B8bCxFSxnW_syqmOXE4GXl3bulmY_yb5_HEDW-vlDm5Pp9mZfwtaEQxMx65DHvylbGXUBqyorGIFDMrBNfJf1H4yNcy9u9MiMxJWZieoxTZEx1w5FIJcTAQpUByYqmALZG6jTyfNcqJs8s2_mu7Y_X_9hDZkPG50CHhZDnne6Y_J8UVbK6SHPT8VCLOTKFmDgs9piuvjTVzbvIZWuK6Y69h85VNnGC5haKAT2Qft3YdO-pa_751GToFlyKUi5ho-KNWJLmrXqw"  # 替换为你要下载的图片URL
# save_directory = "."  # 图片保存目录

# download_image(image_url, save_directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("content")
    options = parser.parse_args()
    print(options.content)