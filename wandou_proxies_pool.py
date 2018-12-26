import json
import requests
from proxypool import ProxiesContainer


class WDProxiesPool:

    def __init__(self):
        self.session = requests.Session()
        self.resourceUrl = 'http://h.wandouip.com/get/ip-list?pack=0&num=20&xy=1&type=2&lb=\r\n&pro=530000&city=532800&port=4&mr=1'
        self.proxiesContainer = ProxiesContainer()
        self.thresholdFloor = 30
        self.thresholdCelling = 70
        self.threshold_based_update()

    def pull_proxies(self):

        raw_data = requests.get(url=self.resourceUrl).text
        proxies_dict_list = json.loads(raw_data).get('data')
        tmp = {}
        for i in proxies_dict_list:
            tmp = {'http':'http://'+i['ip']+':'+str(i['port']), 'expire_time':i['expire_time']}
            self.proxiesContainer.append_proxy(tmp)

    def get_proxy(self):

        return self.proxiesContainer.container.pop()

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
        parsedOrigin = response.json().get('origin')
        if parsedOrigin == self.realIp:
            return False
        return True

    def threshold_based_update(self):

        if self.thresholdFloor > self.proxiesContainer.get_proxies_number():
            self.pull_proxies()






if __name__ == '__main__':

    with requests.Session() as session:

        # session = session.cookies.update()
        page = requests.get(url='http://h.wandouip.com/get/ip-list?pack=0&num=20&xy=1&type=2&lb=\r\n&pro=530000&city=532800&port=4&mr=1')
        proxies_dict_list = json.loads(page.text).get('data')
        f = open('proxies', 'a')
        print(proxies_dict_list)
        for i in proxies_dict_list:
            f.write(i['ip']+':'+str(i['port']))
            f.write('\t'+i['expire_time'])
            f.write('\n')