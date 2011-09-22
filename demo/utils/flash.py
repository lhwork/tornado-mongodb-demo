
from base64 import b64encode, b64decode

class Flash(object):

    def __init__(self, handler):
        self.handler = handler

        try:
            self._error = b64decode(handler.get_cookie('flash_error', None))
        except (TypeError, ValueError):
            self._error = None    

        try:
            self._message = b64decode(handler.get_cookie('flash_message', None))
        except (TypeError, ValueError):
            self._message = None

        handler.clear_cookie('flash_error')
        handler.clear_cookie('flash_message')

    def get_error(self):
        return self._error

    def set_error(self, error):
        self._error = error
        self.handler.set_cookie('flash_error', b64encode(error))

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = message
        self.handler.set_cookie('flash_message', b64encode(message))

    error = property(get_error, set_error)

    message = property(get_message, set_message)

