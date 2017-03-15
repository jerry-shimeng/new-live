import web

urls = (
    "/", "Index",
)
render = web.template.render('templates/')


class Index:
    def GET(self):
        name = "hello world"
        return render.index(name)


class redirect:
    def GET(self, path):
        web.seeother('/' + path)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
