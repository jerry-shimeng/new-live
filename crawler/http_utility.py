import httplib2


class HttpUtility:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        if self.headers is None:
            self.headers = {}
        self.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

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
