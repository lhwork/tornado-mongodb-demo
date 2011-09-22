# -*- coding: UTF-8 -*-

import re

email_re = re.compile(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)",re.IGNORECASE)

def valid_email(email):
    return True if email and email_re.match(email) else False

