import json
import requests
from lxml import etree



def parse_long_string_to_dict(bigstr):
    """get the text of Query String Parameters on Chrome
    transform it to a python dict object"""
    d = {}
    for kv in bigstr.split('\n'):
        kv = kv.split(':')
        k, v = kv[0], kv[-1].lstrip()
        d.setdefault(k, v)
    return d


headersLongStr = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Host: httpbin.org
Pragma: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"""

globalHeaders = parse_long_string_to_dict(headersLongStr)


class ProxiesContainer:

    def __init__(self):

        self.container = []

    def get_proxy(self):

        return self.container.pop()

    def append_proxy(self, proxy):

        return self.container.append(proxy)

    def get_proxies_number(self):

        return len(self.container)

    def get_all_proxies(self):

        return self.container

    def delete_proxy(self, proxy):

        self.container.remove(proxy)


class ProxiesPool:

    global globalHeaders

    def __init__(self, pageNumber=1):

        self.realIp = '1.202.251.26'
        self.camouflage = ''
        self.resourceUrl = 'https://www.xicidaili.com/nn/'
        self.checkStationUrl = 'http://httpbin.org/ip'
        self.pageNumber = pageNumber
        self.proxiesContainer = ProxiesContainer()
        self.thresholdFloor = 40
        self.thresholdCelling = 90
        self.pullFlag = False

    def proxy_is_valid(self, proxy):

        try:
            response = requests.get(url=self.checkStationUrl, proxies=proxy, timeout=3)
            print(response.text)
        except (requests.exceptions.ProxyError,
                requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout):
            return False
        if '有道' in response.text:
            return False
        try:
            parsedOrigin = response.json().get('origin')
        except json.decoder.JSONDecodeError:
            return False
        if parsedOrigin == self.realIp:
            return False
        return True

    def pull_proxies(self):

        page = requests.get(self.resourceUrl, headers=globalHeaders).text
        ele_tree = etree.HTML(page)
        proxy_host_list = ele_tree.xpath('//tr/td[2]/text()')
        proxy_port_list = ele_tree.xpath('//tr/td[3]/text()')
        proxy_type = ele_tree.xpath('//tr/td[6]/text()')
        for i in zip(proxy_host_list, proxy_port_list, proxy_type):
            proxy_dict = {i[2].lower(): i[2].lower()+"://"+i[0]+':'+i[1]}
            self.proxiesContainer.append_proxy(proxy_dict)

    def get_proxy(self):

        return self.proxiesContainer.container.pop()

    def threshold_based_update(self):

        if self.thresholdFloor > self.proxiesContainer.get_proxies_number():
            self.pull_proxies()
            self.pageNumber += 1
        for i in self.proxiesContainer.container:
            if not self.proxy_is_valid(i):
                self.proxiesContainer.container.remove(i)


if __name__ == '__main__':

    proxiesPool = ProxiesPool()
    proxiesPool.pull_proxies()
    print(len(proxiesPool.proxiesContainer.container))
    ps = proxiesPool.proxiesContainer.container
    print(ps)
    f = open('some_proxies', 'a')
    for i in ps:
        if proxiesPool.proxy_is_valid(i):
            print(i)
            f.write(str(proxiesPool.get_proxy()))
            f.write('\n')
    aproxy = proxiesPool.get_proxy()
    print(proxiesPool.proxy_is_valid(aproxy))

