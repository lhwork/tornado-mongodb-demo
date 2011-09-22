import smtplib
import tornado.web

from tornado.options import options
from tornado.web import HTTPError

from email.mime.text import MIMEText

from demo.core.database import MongoDB
from demo.utils.flash import Flash
from demo.utils.mail import Mailer

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.flash = Flash(self)
        self.database = MongoDB.db.database

    def get_current_user(self):
        email = self.get_secure_cookie("email")
        return self.database.users.User.find_one({'email': email})

    def send_email(self, to_addr, subject, template, *args, **kwargs):
        body = self.render_string(template, *args, **kwargs)
        Mailer.send_mail(to_addr, subject, body)


