from tornado.options import define

define('debug', default=False, help='enable autoreload for tornado web apps', type=bool)
define("mode", default="development", help="run in development or production mode")

define("port", default=8888, help="tornado listen port", type=int)

define("static_path", default='resources', help="define the path for the app")
define("template_dir", default='/tmp/views', help="set the dir for mako to look for templates")

define("db_host", default='localhost', help="connect to the db on this host")
define("db_port", default=27017, help="connect to the db on this port", type=int)
define("db_name", default="demo", help="the name of the database to use")

define('smtp_host', default='localhost', help='smtp server host')
define('smtp_port', default=25, help='smtp server port')
define('smtp_username', default='', help='smtp server username')
define('smtp_password', default='', help='smtp server password')
define('smtp_from', default='', help='smtp server mail from')

define("cookie_secret", default="mehungryforcookie", help="cookie secret for tornado secure cookies")

define("login_url", default="/login", help="whats the login url")

define("log", default="", help="the logfile")

