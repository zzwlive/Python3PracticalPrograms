#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 21:58
# @Author  : cunyu
# @Site    : cunyu1943.github.io
# @File    : maoyanMovieRank.py
# @Software: PyCharm

"""
使用正则表达式提取猫眼电影排行榜
"""

import json
import requests
from requests.exceptions import RequestException
import re
import time


# 获取其中一页的网页信息
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 对获取到的网页信息进行解析
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '海报': item[1],
            '电影名': item[2],
            '演员': item[3].strip()[3:],
            '时长': item[4].strip()[5:],
            '评分': item[5] + item[6]
        }

# 将电影信息写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

# 定义主程序
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)

