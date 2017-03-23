#coding=utf-8
import tornado
import traceback

class HtmlHandler(tornado.web.RequestHandler):
    def get(self,name):
        try:
            self.render(name)
        except:
            traceback.print_exc()
            self.set_status(500)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('index.html')