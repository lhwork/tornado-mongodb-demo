import datetime
import logging
import os

class Log():

    instance = None

    def __init__(self, log_file=''):
        dirname, filename = os.path.split(log_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.file_logger = logging.getLogger('demo')
        hdlr = logging.FileHandler(log_file)
        hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(user)s %(message)s %(extended_info)s'))
        self.file_logger.addHandler(hdlr)
        self.file_logger.setLevel(logging.DEBUG)

    def __new__(type, *args, **kwargs):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type, *args, **kwargs)
        return type._instance

    def message(self, type, message, user='', extended_info=''):
        getattr(self.file_logger, type)(message, extra={'user':user, 'extended_info':extended_info})

    @staticmethod
    def create(log_file=''):
        Log.instance = Log(log_file)

    @staticmethod
    def info(message, user=''):
        Log.instance.message('info', message, user)

    @staticmethod
    def debug(message, user=''):
        Log.instance.message('debug', message, user)

    @staticmethod
    def error(message, user=''):
        Log.instance.message('error', message, user)

    @staticmethod
    def warning(message, user=''):
        Log.instance.message('warning', message, user)

    @staticmethod
    def critical(message, user=''):
        Log.instance.message('critical', message, user)

