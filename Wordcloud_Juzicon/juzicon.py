# -*- coding: utf-8 -*-
import re

import jieba
import requests
from bs4 import BeautifulSoup
import wordcloud
from matplotlib import pyplot


# 获取html
def get_html(url):
    headers = {
        'Host': 'www.juzikong.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.109 Safari/537.36',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except TimeoutError:
        return None


# 解析网页 获取json
def get_detail_html(data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.109 Safari/537.36',
        'DNT': '1',
        'Origin': 'https://www.juzikong.com',
        'Referer': 'https://www.juzikong.com/',
        'Accept': 'application/json, text/plain, */*',
    }
    url = 'https://api.juzikong.com/n0/home/posts/recommend?start='
    response = requests.get(url, headers=headers, params=data)
    response.encoding = response.apparent_encoding
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except TimeoutError:
        return None


# 解析首页
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    contents = soup.findChildren('div', class_='body_2oAQz')
    for content in contents:
        dirt = {}
        text = content.find('a', class_='contentLink_1mEsJ').text.strip().replace('\n', '。').replace(' ', '')
        dirt['句子'] = text
        try:
            author = content.find('div', class_='source_2RP0v').text.strip().replace('\n', '')
        except AttributeError:
            author = None
        dirt['作者'] = author
        yield dirt


# 得到首页句子和作者
def get_data():
    url = 'https://www.juzikong.com/'
    html = get_html(url)
    list = []
    for content in parse_html(html):
        list.append(content)
    return list


# 获取第二页及以后的页面的句子和作者，通过json获取
def parse_detail(num):
    num *= 10
    json = get_detail_html(num)
    lists = json['data']['list']
    data = []
    for list in lists:
        dirt = {'句子': list['content'].replace('\n', ''), '作者': list['referAuthorName']}
        data.append(dirt)
    return data


# 分词
def cutting_word(words):
    counts = []
    for word in words:
        # 筛选掉单个字符
        #   if len(word) == 1:
        #      continue
        counts.append(word)
    return counts


# 生成词云
def drawing_wordcloud(data):
    ls = ' '.join(data)
    w = wordcloud.WordCloud(background_color='white', width=1400, height=1600, font_path='./fonts/simhei.ttf').generate(
        ls)
    pyplot.imshow(w)
    pyplot.axis('off')
    pyplot.show()


if __name__ == '__main__':
    data = []
    data += get_data()
    for num in range(1, 50):        # 获取第二页到第50页内容
        data += parse_detail(num)

    words = []
    for da in data:
        word = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！：，。？?、~@#￥%……&*（）]+", "", da['句子'])    # 通过正则表达式去除句子中的标点符号
        words += jieba.lcut(str(word))

    cloud = cutting_word(words)
    drawing_wordcloud(cloud)
