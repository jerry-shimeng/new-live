from bs4 import BeautifulSoup
import httplib2

import socks
from http_utility import HttpUtility

url = 'http://www.kuaidaili.com/free/inha/'
features = "lxml"


class ProxyParser(object):
    @classmethod
    def run(cls):
        html = HttpUtility(url).get()
        cls.start(html)

    @classmethod
    def start(cls, html):
        soup = BeautifulSoup(html, features)
        trs = soup.find("table").find("tbody").find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) < 3:
                continue
            host = tds[0].string
            port = tds[1].string
            cls.test(host, port)
            print(host, ":", port)

    @classmethod
    def test(cls, host, port):
        hp = httplib2.Http(proxy_info=httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, host, port))
        h, c = hp.request("http://www.facebook.com")
        print(h, "\n", c)
