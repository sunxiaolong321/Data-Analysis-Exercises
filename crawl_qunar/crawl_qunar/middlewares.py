# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class ProxyMiddleWare(object):
     # 从数据库中随机取一个代理IP，每次请求的时候都使用代理

    def process_request(self, request, spider):
        def GetHtml():
            import requests

            def get_proxy():
                return requests.get("http://127.0.0.1:5010/get/").json()

            def delete_proxy(proxy):
                requests.get(
                    "http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

            def get_html():
                # ....
                retry_count = 5
                proxy = get_proxy().get("proxy")
                while retry_count > 0:
                    try:
                        html = requests.get('https://www.baidu.com',
                                            proxies={"http": "http://{}".format(proxy)})
                        # 使用代理访问
                        return proxy
                    except:
                        retry_count -= 1
                # 出错5次, 删除代理池中代理
                delete_proxy(proxy)
                return get_html()

            return get_html()
        proxy = GetHtml()
        if proxy != None:
            request.meta['proxy'] = 'http://%s' % proxy

    # 每次异常的时候使用代理
    # def process_exception(self, request, response, spider):
    #     request.meta['proxy'] = self.GetHtml()


class UserAgentMiddleWare(object):
    def process_request(self, request, spider):
        from fake_useragent import UserAgent
        ua = UserAgent()
        request.headers['USER_AGENT'] = ua.random
