import smtplib
import tornado.web

from tornado.options import options
from tornado.web import HTTPError

from email.mime.text import MIMEText

from pymongo.errors import DuplicateKeyError

from demo.utils.decorators import route
from demo.core.request import BaseHandler
from demo.web.models.user import User, ResetRequest

@route('/')
class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        self.render('index.html', user=user)

@route('/signup')
class SignupHandler(BaseHandler):
    def get(self):
        next = self.get_argument('next', '/')
        self.render('signup.html', next=next)

    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)

        if not email or not password:
            self.flash.error = "You must enter a email and password to proceed. Please try again."
            self.redirect("/signup")
            return

        if password != self.get_argument("password2", None) :
            self.flash.error = "Passwords do not match. Please try again."
            self.redirect("/signup")
            return

        user = self.database.users.User()
        user.email = email
        user.set_password(password)
        user.save()
        self.flash.message = "Successfully created your account, please log in."
        self.redirect("/login")

@route('/login')
class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('login.html')

    def post(self):
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)
        try:
            self.authenticate(email, password)
            self.redirect('/')

        except ValueError, e:
            self.flash.error = str(e)
            self.render('login.html')

    def authenticate(self, email, password):
        if not email or not password:
            raise ValueError('Both fields are mandatory.')

        email = email.lower()
        record = self.database.users.User.find_one({'email': email})

        if record and record.is_valid_password(password):
            if record.active:
                self.set_secure_cookie('email', record.email)
                return True
            else:
                raise ValueError('Deactivated Account.')
        raise ValueError('Invalid credentials.')

@route('/logout')
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('email')
        self.redirect('/login')

@route('/password/reset')
class RequestResetHandler(BaseHandler):
    def get(self):
        self.render('request_reset.html')

    def post(self):
        email = self.get_argument('email', None)
        try:
            self.prepare_reset(email)
            self.flash.message = 'The reset email was sent. Check your inbox.'

        except ValueError, e:
            self.flash.error = str(e)

        self.render('request_reset.html', page='reset')

    def prepare_reset(self, email):
        #if not email or not valid_email(email):
        #  raise ValueError('Invalid email address')

        email = email.lower()
        if not self.database.users.User.find_one({'email': email}):
            raise ValueError('No account found for this email address')

        key = self.generate_reset_key(email)
        reset_url = '%s://%s/password/change/%s' % (self.request.protocol, self.request.host, key)

        self.send_email(email,
            'noreply@example.com',
            'Password Reset',
            'emails/reset.txt',
            reset_url = reset_url
        )

    def generate_reset_key(self, email):
        """ Try until the generated one is unique """
        while True:
            try:
                r = self.database.reset.ResetRequest()
                r.email = email
                r.save()
                return r.key

            except DuplicateKeyError:
                pass

@route('/password/change/(.*)')
class PasswordResetHandler(BaseHandler):
    def get(self, key):
        if not self.get_user(key):
            raise HTTPError(401)

        self.render('password_reset.html', key=key)

    def post(self, key):
        new, repeat = self.get_argument('new', None), self.get_argument('repeat', None)
        try:
            self.change_password(new, repeat, key)
            self.redirect('/login')

        except ValueError, e:
            self.flash.error = str(e)

        self.render('password_reset.html', key=key)

    def change_password(self, new, repeat, key):
        user = self.get_user(key)
        if not user: raise HTTPError(401)

        if not new or not repeat:
            raise ValueError('All fields are mandatory')

        if new != repeat:
            raise ValueError('Passwords do not match')

        user.set_password(new)
        user.save()

        self.database.reset.remove({'key': key})

    def get_user(self, key):
        r = self.database.reset.ResetRequest.find_one({'key':key})
        if not r: return None

        return self.database.users.User.find_one({'email': r.email})

