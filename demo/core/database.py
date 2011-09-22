from tornado.options import options
from mongokit import Connection

from demo.utils import randchars
from demo.core.log import Log

class MongoDB(object):

    db = None

    def __init__(self):
        self.conn = None

    def __new__(type, *args, **kwargs):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type, *args, **kwargs)
        return type._instance

    def register_models(self, models=[]):
        self.conn.register(models)

    @property
    def database(self):
        return self.conn[options.db_name]

    @staticmethod
    def create(host=None, port=None):
        if not host and not port:
            try:
                host, port = options.db_host, options.db_port
            except (AttributeError, ValueError):
                host, port = None, None

        if host and port:
            db = MongoDB()
            db.conn = Connection(host, int(port))
            MongoDB.db = db
            Log.debug("MongoDB server %s." % MongoDB.db.conn)
        else:
            raise Exception('You need to configure the host and port of the MongoDB document server.')


