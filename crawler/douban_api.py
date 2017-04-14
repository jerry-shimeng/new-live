import json

import httplib2

# api doc https://developers.douban.com/wiki/?title=movie_v2#subject
base_url = "https://api.douban.com"
search_url = base_url + "/v2/movie/search?q=%s"
detail_url = base_url + "/v2/movie/subject/%d"


class DoubanApi:
    @classmethod
    def run(cls):
        pass

    @classmethod
    def get(cls, url):
        http = httplib2.Http()
        h, content = http.request(url)
        return content.decode("utf-8")

    @classmethod
    def search(cls, name):
        url = search_url % name
        content = cls.get(url)
        obj = json.loads(content)
        if obj["total"] == 0:
            print("not result for ", name)
            return

        for a in obj["subjects"]:
            if name.__contains__(a["title"]) or a["title"].__contains__(name):
                print(a["id"])
                return int(a["id"])
        return 0

    @classmethod
    def detail(cls, id):
        if id == 0:
            return None
        url = detail_url % id
        content = cls.get(url)
        print(content)


if __name__ == "__main__":
    name = "铁道飞虎"
    id = DoubanApi.search(name)
    DoubanApi.detail(id)
