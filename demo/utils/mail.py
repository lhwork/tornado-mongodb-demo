# -*- coding: UTF-8 -*-

import email
import smtplib

from tornado.options import options

class Mailer:

    instance = None

    def __init__(self, smtp_host, smtp_user, smtp_password, smtp_port=25):
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_port = smtp_port
        self.mail = email.MIMEMultipart.MIMEMultipart('related')
        self.alter = email.MIMEMultipart.MIMEMultipart('alternative')
        self.mail.attach(self.alter)
        self.attachments = []

    def __new__(type, *args, **kwargs):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type, *args, **kwargs)
        return type._instance

    def mail_from(self, mail_from):
        self._from = mail_from
        self.mail['from'] = mail_from

    def mail_to(self, mail_to):
        self._to = mail_to
        if type(mail_to) == list:
            self.mail['to'] = ','.join(mail_to)
        elif type(mail_to) == str:
            self.mail['to'] = mail_to
        else:
            raise Exception('invalid mail to')

    def subject(self, subject):
        self.mail['subject'] = subject

    def body(self, body, body_type='plain', encoding='utf-8'):
        self.alter.attach(email.MIMEText.MIMEText(body, body_type, encoding))

    def attach(self, file_path, mime_type='octect-stream', rename=None):
        import os
        f = open(file_path, 'rb')
        file_content = f.read()
        f.close()
        mb = email.MIMEBase.MIMEBase('application', mime_type)
        mb.set_payload(file_content)
        email.Encoders.encode_base64(mb)
        fn = os.path.basename(file_path)
        mb.add_header('Content-Disposition', 'attachment', filename=rename or fn)
        self.mail.attach(mb)

    def send(self):
        self.mail['Date'] = email.Utils.formatdate( )
        smtp = False
        try:
            smtp = smtplib.SMTP()
            smtp.set_debuglevel(0)
            smtp.connect(self.smtp_host, self.smtp_port)
            smtp.login(self.smtp_user, self.smtp_password)
            smtp.sendmail(self._from, self._to, self.mail.as_string())
            return True
        except Exception, e:
            import traceback
            print traceback.format_exc()
            return False
        #finally:
        smtp and smtp.quit()

    @staticmethod
    def create_mailer():
        _instance = Mailer(options.smtp_host, options.smtp_username, options.smtp_password)
        _instance.mail_from(options.smtp_from)
        Mailer.instance = _instance

    @staticmethod
    def send_mail(mailto, subject, body, body_type):
        Mailer.instance.mail_to(mailto)
        Mailer.instance.subject(subject)
        Mailer.instance.body(body, body_type)
        Mailer.instance.send()


