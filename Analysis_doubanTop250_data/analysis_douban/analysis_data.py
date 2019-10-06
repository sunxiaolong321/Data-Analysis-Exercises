import os

import matplotlib.pyplot as plt
# import matplotlib.style as mplstyle
import numpy as np
import pandas as pd


# 柱状图显示拍摄国家
def plot_nation(data, path=os.getcwd()):
    plt.figure(figsize=(10, 6), dpi=300)
    nation_count = data['nation'].value_counts()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    nation_count.plot(kind='bar', title='豆瓣top250拍摄国家统计',
                      fontsize=7, grid='True', color='g')
    nation_count.plot(kind='line', marker='o', color='r')
    plt.grid(linestyle='-.')
    plt.tight_layout()  # 自动调节合适大小
    plt.savefig('chart&data/国家统计.png', dpi=300,)  # 保存图片
    plt.show()

# 饼形图显示拍摄国家


def average_star(data, path=os.getcwd()):
    plt.figure(figsize=(10, 6), dpi=300)
    star = data['star'].value_counts()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    star.plot(kind='pie', title='豆瓣top250评分', fontsize=7, legend='True')
    plt.tight_layout()  # 自动调节合适大小
    plt.savefig(path+'分数统计.png', dpi=300,)  # 保存图片
    plt.show()

# 柱状图显示拍摄国家，将国家拆分


def plot_nation_person(data, path=os.getcwd()):

    # 这是一个坑，pandas.DataFrame.value_counts() 会返回一个pandas.Series
    nation = data['nation'].value_counts()

    dict_nations = nation.to_dict()
    new_nations = dict_nations.copy()

    for key, value in dict_nations.items():
        if '/'in key:
            countrys = key.split('/')
            for country in countrys:
                new_nations[country] = new_nations.get(
                    country, 0)+value
            new_nations.pop(key)

    plt.figure(figsize=(30, 50), dpi=300)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.title('top250优质电影国家数目', fontsize=50)
    plt.subplot(211)
    plt.bar(range(len(new_nations)), new_nations.values(), width=0.8,
            tick_label=list(new_nations.keys()), color='seagreen', alpha=0.8)
    plt.xticks(rotation=90)
    i = 0
    for key, value in new_nations.items():
        plt.text(i, value, '%.0f' %
                 value, ha='center', va='bottom', fontsize=20)
        i += 1
    plt.yticks(np.linspace(0, 150, 11), fontsize=20)
    plt.tight_layout()
    plt.subplot(212)
    patches, l_text, p_text = plt.pie(new_nations.values(
    ), labels=new_nations.keys(), autopct='%1.2f%%', startangle=90, pctdistance=0.9)
    # 改变文本的大小, 方法是把每一个text遍历。调用set_size方法设置它的属性
    for t in l_text:
        t.set_size = (5)
    for t in p_text:
        t.set_size = (5)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(path+'国家影片数量.png', dpi=300,)  # 保存图片
    plt.show()


def group_type(data, path):
    lis = []
    for key, value in data.groupby('nation')['type']:
        dic = {}
        for va in value.values:
            for v in va.split('/'):  # 将series分开
                word = v[:2]
                if word in ['传记', '儿童', '冒险', '剧情', '动作', '动画', '历史', '古装',
                            '同性', '喜剧', '奇幻', '家庭', '恐怖', '悬疑', '情色', '惊悚', '战争', '歌舞', '武侠', '灾难', '爱情', '犯罪'
                            '科幻', '纪录', '西部', '运动', '音乐']:
                    dic[word] = dic.get(word, 0)+1
        for ke in key.split('/'):
            lis.append(pd.DataFrame(dic, index=[ke]))
        # daf = pd.DataFrame(dic, index=[key])  # 把字典添加到daf
        # print(daf)
        # lis.append(daf)
    # print(lis)
    result = pd.concat(lis, sort=True)
    res = result.fillna(0).groupby(level=0).sum()

    # plt.figure(figsize=(20,50),dpi=300)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.subplot(111)
    res.plot(kind='bar', title='豆瓣top250电影类别数量统计',
             fontsize=7, figsize=(15, 6), grid=True, legend=True)
    plt.legend(loc='best', ncol=3, fontsize='medium')
    # res.table()
    # mplstyle.use('fast')
    # plt.table()
    plt.tight_layout()
    plt.savefig(path+'Bar&DoubanTOP250 Number Of Movie Category.png', dpi=300)
    plt.show()
    # daf_sum[key] = dic


def release_language(data, path):

    lan = data['language'].value_counts()
    dict_lan = lan.to_dict()
    new_lan = dict_lan.copy()
    # print(new_lan)
    for key, value in dict_lan.items():
        if '/'in key:
            lans = key.split('/')
            for lan in lans:
                new_lan[lan] = new_lan.get(lan, 0)+value
            new_lan.pop(key)
    del dict_lan
    # print(new_lan)
    plt.figure(figsize=(20, 35), dpi=300)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.subplot(211)
    plt.bar(range(len(new_lan)), new_lan.values(), width=0.8,
            tick_label=list(new_lan.keys()), color='b', alpha=0.8)
    plt.grid(alpha=0.6, color='grey', linestyle='-.', linewidth=3)
    plt.xticks(rotation=90)
    i = 0
    for key, value in new_lan.items():
        plt.text(i, value, '%.0f' %
                 value, ha='center', va='bottom', fontsize=20)
        i += 1
    plt.yticks(np.linspace(0, 170, 18), fontsize=40)

    plt.subplot(212)
    new_other_lan = new_lan.copy()
    for key, value in new_other_lan.items():
        if value < 5:
            new_lan['other'] = new_lan.get('other', 0)+value
            new_lan.pop(key)
    # print(new_lan)
    del new_other_lan
    x, l_text, p_text = plt.pie(new_lan.values(), labels=new_lan.keys(),
                                autopct='%1.2f%%', startangle=90, pctdistance=0.9)
    for t in l_text:
        t.set_fontsize = (100)
    for t in p_text:
        t.set_fontsize = (100)
    plt.legend(loc='upper right', fontsize='medium')
    plt.tight_layout()
    plt.savefig(path+'Douban Top250 of language range.png', dpi=300)
    plt.show()


def release_time(data, path):
    pass


def format_date(data, path):
    df = pd.DataFrame(data)
    # 将名称一列作为index
    df.set_index('name', inplace=True)

    # 计算data中国家出现次数
    # plot_nation(df, path)
    # average_star(df, path)
    # plot_nation_person(df, path)
    # group_type(df, path)
    # df.to_excel(path+'原始数据.xlsx')
    release_language(df, path)
    pass
