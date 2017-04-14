import json

import httplib2

from commmon import DatetimeJSONEncoder


class HttpUtility:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        if self.headers is None:
            self.headers = {}
        self.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        self.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        self.headers["Host"] = "www.kuaidaili.com"
        self.headers["Referer"] = "http://www.kuaidaili.com/free/outtr/"
        self.headers[
            "Cookie"] = "_ydclearance=64a19e4f7de1511451fc0cac-7bd2-4f46-98b0-cfb596c4fd05-1491821780; _ga=GA1.2.14556732.1491814584; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1491814584; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1491815618; channelid=0; sid=1491815787620643"

    def get(self, recall=False, encoding='utf-8'):
        try:
            return self.get_not_decode().decode(encoding)
        except UnicodeDecodeError as e:
            if not recall:
                return self.get(recall=True, encoding="ISO-8859-1")
            else:
                print(e)
                return ""
        except TimeoutError:
            return ""

    def get_not_decode(self):
        h = httplib2.Http()
        (req_headers, content) = h.request(self.url, method="GET", body=None, headers=self.headers)
        return content

    @classmethod
    def post(cls, address, data, headers=None, encoding='utf-8'):
        body = None
        if type(data) is str:
            body = data
        else:
            body = json.dumps(data, cls=DatetimeJSONEncoder)

        h = httplib2.Http()

        # body = bytes(body,encoding="utf-8")
        print(body)
        (req_headers, content) = h.request(address, method="POST", body=body)
        return content.decode(encoding)
