import re
import enum
import pandas as pd
import urllib.request
import os

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from PIL import Image
import pathlib
from pathlib import Path


class PictureInfo(enum.Enum):
    INDEX = 'index'
    TITLE = 'title'
    LINK = 'src'


# 爬取的数据持久化为文件
def data_write_csv(file_path_name, datas):  # file_name为写入CSV文件的路径，datas为要写入数据列表
    df = pd.DataFrame()
    # list(dict)转dataframe
    for ele in datas:
        df = pd.concat([df, pd.DataFrame(ele, index=[ele['index']])])
    df.to_csv(file_path_name, encoding='utf_8_sig')
    print("本地文件持久化完成")


# 图片转jpg
def webp_to_jpg(jpg_path_name):
    for idx, f in enumerate(pathlib.Path(Path(jpg_path_name).joinpath("webp")).glob("*.webp"), start=1):
        print(f"正在转码第 {idx} 张图片")
        img = Image.open(f)
        # -5是按照.webp刚好5个字符得出的 其他格式需要改
        # 注意Windows下分隔符和Linux不同
        file_name = str(f)[0:-5].split("\\").pop() + ".jpg"
        # img.load(), img.save(f[0:-5] + ".jpg")
        img.load(), img.save(Path(jpg_path_name).joinpath(file_name))
        # remove(f)
    print("图片转码完成")


def crawler(gallery_id):
    base_url = ""
    # 定义headers信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.12022 SLBChan/103'}

    req = Request(base_url + gallery_id + ".html", headers=headers)
    resp = urlopen(req)
    # file = open("C:/Users/BlueCitizen/Desktop/test.html", "rb")
    # html = file.read().decode("utf-8")
    html = resp.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")

    # 抓取图集的标题
    gallery_title = bs.find_all(class_="title")[0].next_element.next
    print(gallery_title)
    gallery_path = "E:/crawler/" + gallery_title + "/"
    if os.path.exists(gallery_path):
        print(f'文件夹 {gallery_path} 已存在')
    else:
        os.mkdir(gallery_path)
    # 抓取分页的总页数
    pc = re.compile(r"\d+")
    page_count = pc.search(str(bs.find_all(class_="paging")[0].next_element)).group()

    # 抓取所有图片的地址 这是特定网站的url索引拼接结构
    gallery = gallery_id.split("-")
    picture_list = []
    picture_count = 0
    for i in range(0, int(page_count)):
        # 最后一位退栈
        gallery.pop()
        gallery.append(str(i))
        gallery_id = '-'.join(gallery)
        current_url = base_url + gallery_id + ".html"
        print("当前处理的页面地址 " + current_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.12022 SLBChan/103'}

        req = Request(current_url, headers=headers)
        resp = urlopen(req)
        html = resp.read().decode("utf-8")
        bs = BeautifulSoup(html, "html.parser")
        main = bs.find_all(class_="main")[0]
        # 解析main部分的children 里面是图片序列
        cdr = main.children
        for idx in cdr:
            picture_count = picture_count + 1
            ele = idx.next.attrs
            del ele['alt']
            ele[PictureInfo.INDEX.value] = picture_count
            picture_list.append(ele)

    # 保存爬取的图片地址到本地csv文件
    data_write_csv(gallery_path + "category.csv", picture_list)

    if os.path.exists(gallery_path + "webp/"):
        print(f'文件夹 {gallery_path + "webp/"} 已存在')
    else:
        os.mkdir(gallery_path + "webp/")

    # 抓取图片到创建的目录下
    for el in picture_list:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36'}
        pic_req = urllib.request.Request(el[PictureInfo.LINK.value], headers=headers)
        pic_page = urllib.request.urlopen(pic_req)
        pic_bytes = pic_page.read()
        print(f"正在抓取第 {el['index']}/{picture_count} 张图片")
        with open(gallery_path + "webp/" + str(el[PictureInfo.INDEX.value]) + ".webp", "wb") as f:
            f.write(pic_bytes)

    # 转换webp到jpg格式
    webp_to_jpg(gallery_path)


if __name__ == '__main__':
    crawler("")
