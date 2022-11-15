#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, logging
from assemble import assemble
from diffuse import diff_apk
from files import *
from apktool import ApkInfo
from logger import config_logging
from git_tag import *
from global_config import *
from strengthen import jiagu_360
from mailing import send_email
from resources import *

def _build_apk(bit: BitConfiguration, flavor: FlavorConfiguration) -> ApkInfo:
    '''Execute APK build flow.'''
    info = assemble(bit, flavor)
    diff = diff_apk(info)
    jiagu_file_directory = os.path.join(info.output_apk_directory, 'strengthen')
    jiagu_360(info.output_apk_file_path, jiagu_file_directory)
    mail_subject = "%s(%s,%s)" % (config.output_mail_title, flavor.get_name(), bit.get_name())
    send_email(config.output_mail_receivers, mail_subject, diff, 'html')
    return info

if __name__ == "__main__":
    config_logging()
    info = _build_apk(BitConfiguration.BIT_64, FlavorConfiguration.NATIONAL)
    info = _build_apk(BitConfiguration.BIT_64, FlavorConfiguration.OVERSEA)
    copy_language_resources(info.version_name)
    gen_git_log(info)
    add_new_tag(info)
