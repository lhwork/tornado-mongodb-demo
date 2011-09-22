import datetime
import time

from hashlib import sha256

from demo.web.models.base import BaseDocument
from demo.utils import randchars
from demo.utils.validators import valid_email
from demo.core.database import MongoDB

@MongoDB.db.conn.register
class User(BaseDocument):
    structure = {
        'email': unicode,
        'password': unicode,
        'salt': unicode,
        'created': datetime.datetime,
        'active': bool
    }
    required_fields = ['email', 'password', 'salt']
    default_values = {
        'created': datetime.datetime.utcnow,
        'active': True
    }
    validators = {
        'email': valid_email,
    }
    indexes = [
        {'fields': ['email'], 'unique': True},
    ]

    def set_password(self, password):
        self.salt = unicode(randchars(32))
        self.password = unicode(sha256(password + self.salt).hexdigest())

    def is_valid_password(self, password):
        return self.password == unicode(sha256(password + self.salt).hexdigest())

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

@MongoDB.db.conn.register
class ResetRequest(BaseDocument):
    structure = {
        'email': unicode,
        'key': unicode,
        'created': datetime.datetime
    }
    required_fields = ['email', 'key', 'created']
    default_values = {
        'created': datetime.datetime.utcnow,
        'key': lambda: unicode(randchars(16))
    }
    indexes = [
        {'fields': ['key'], 'unique': True}
    ]

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(ResetRequest, self).save(*args, **kwargs)

