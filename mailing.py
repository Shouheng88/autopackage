#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, traceback, logging
from email.header import Header
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from typing import *
from logger import config_logging
from global_config import *

def send_email(receivers: List[str], subject: str, message: str, mail_type: str = 'plain', filename = None):
    '''Send email tool.'''
    from_ = "Android自动打包脚本<%s>" % config.mail_user
    to_ = ';'.join(['Manager<%s>' % email_ for email_ in receivers])
    msg = MIMEMultipart()
    msg['From'] = _format_addr(from_)
    msg['To'] =  _format_addr(to_)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(MIMEText(message, mail_type, 'utf-8'))
    if filename is not None:
        with open(filename, 'rb') as f:
            mime = MIMEBase('text', 'txt', filename='error.log')
            mime.add_header('Content-Disposition', 'attachment', filename='error.log')
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com')
        smtpObj.login(config.mail_user, config.mail_password)
        smtpObj.sendmail(config.mail_user, receivers, msg.as_string())
        logging.info("Succeed to send email.")
    except BaseException as e:
        print("Failed to send email:\n%s" % traceback.format_exc())

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

if __name__ == "__main__":
    '''Test entry.'''
    config_logging()
    config.parse()
    print(config.mail_receivers)
    print(config.mail_user)
    print(config.mail_password)
    send_email(config.mail_receivers, "测试", "测试")
