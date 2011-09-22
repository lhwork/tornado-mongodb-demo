
from tornado.web import Application
import os
import sys

class App(Application):

    def __init__(self):
        pass

    def init_path(self):
        parent_dir, dir = os.path.split(sys.path[0])
        sys.path.insert(0, parent_dir)

    def init_logging(self, log):
        from core.log import Log
        Log.create(log)

    def init_routes(self):
        import pkgutil
        import web.handlers
        from utils.decorators import route
        from config.urls import routes

        package = web.handlers
        prefix = package.__name__ + "."

        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__(modname)

        url_routes = route.get_routes()

        url_routes.extend(routes)

        return url_routes

    def main(self):
        import tornado.web
        import tornado.httpserver
        import tornado.ioloop
        import tornado.options
        from tornado.options import options
        import config.options
        from core.log import Log
        from core.database import MongoDB
        from utils.mail import Mailer

        tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__),'config/settings.py'))
        tornado.options.parse_command_line()

        self.init_logging(options.log)

        MongoDB.create(host=options.db_host, port=options.db_port)

        Mailer.create_mailer()

        url_routes = self.init_routes()

        settings = dict(
            template_path = options.template_dir,
            static_path = options.static_path,
            cookie_secret = options.cookie_secret,
            login_url = '/login',
            debug = options.debug
        )


        http_server = tornado.httpserver.HTTPServer(tornado.web.Application(url_routes, **settings))

        http_server.listen(options.port)

        Log.info("Ready and listening")

        tornado.ioloop.IOLoop.instance().start()

    @staticmethod
    def run():
        app = App()
        app.main()


