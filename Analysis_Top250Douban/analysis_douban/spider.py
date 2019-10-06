import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def crawl_url(url, params=None):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        response = s.get(url, params=params, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except TypeError:
        print('抓取{}失败'.format(url))


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for detail in soup.find_all('div', class_='hd'):
        yield [''.join(detail.find('a').text.split()), detail.find('a').get('href')]


def parse_details(html):
    soup = BeautifulSoup(html, 'lxml')

    detail = {
        'director': None,
        'editor': None,
        'actor': None,
        'type': None,
        'nation': None,
        'language': None,
        'show_time': None,
        'duration': None,
        'star':None
    }
    detail_str = soup.find('div', id='info').text
    detail_str = ''.join(detail_str.split())
    # print(soup.find('strong',class_=['ll', 'rating_num']))
    detail['star'] = soup.find('strong',class_=['ll', 'rating_num']).text
    pattern = re.compile(
        r'导演:(.*)编剧:(.*)主演:(.*)类型:(.*)制片国家/地区:(.*)语言:(.*)上映日期:(.*)片长:(.*)分钟.*')
    strings = pattern.search(detail_str)
    if strings:
        detail['director'] = strings.group(1)
        detail['editor'] = strings.group(2)
        detail['actor'] = strings.group(3)
        detail['type'] = strings.group(4)
        detail['nation'] = strings.group(5)
        detail['language'] = strings.group(6)
        detail['show_time'] = strings.group(7)
        detail['duration'] = strings.group(8)
    else:
        pattern = re.compile(
            r'导演:(.*)类型:(.*)制片国家/地区:(.*)语言:(.*)上映日期:(.*)片长:(.*)又名.*')
        strings = pattern.search(detail_str)
        if strings:
            detail['director'] = strings.group(1)
            detail['type'] = strings.group(2)
            detail['nation'] = strings.group(3)
            detail['language'] = strings.group(4)
            detail['show_time'] = strings.group(5)
            detail['duration'] = strings.group(6)
        else:
            pattern = re.compile(
                r'导演:(.*)编剧:(.*)类型:(.*)官方.*制片国家/地区:(.*)语言:(.*)上映日期:(.*)片长:(.*)又名.*')
            detail['director'] = strings.group(1)
            detail['editor'] = strings.group(2)
            detail['type'] = strings.group(3)
            detail['nation'] = strings.group(4)
            detail['language'] = strings.group(5)
            detail['show_time'] = strings.group(6)
            detail['duration'] = strings.group(7)
    return detail


def require_data(urls, count, page):

    data = []

    for i in tqdm(range(0, count, page)):
        params = {
            'start': i,
            'filter': None,
        }

        for name, url in parse_html(crawl_url(urls, params)):
            dic = parse_details(crawl_url(url))
            dic['name'] = name
            data.append(dic)
    print('抓取数据成功')
    return data
