import sys
app_path = sys.path[0]

debug = True
mode = "development"

port = 8000

static_path = "%s/static" % app_path
template_dir = "%s/demo/web/templates" % app_path

log = "%s/logs/demo.log" % app_path

db_host = 'localhost'
db_port = 27017
db_name = 'demo'

smtp_host = 'localhost'
smtp_port = 25
smtp_username = ''
smtp_password = ''
smtp_from = ''

cookie_secret = "setthistoyourowncookiesecret"

