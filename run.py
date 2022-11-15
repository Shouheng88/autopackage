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

def _copy_language_resources(version_name: str):
    '''Copy language resources to community repo and push to github.'''
    # TODO prase xml files and find strings added 
    app_language_dir = os.path.join(config.output_languages_directory, version_name)
    any_new_resources = False
    for values_dir in os.listdir('../app/src/main/res/'):
        if values_dir.startswith('values'):
            dir_path = os.path.join(app_language_dir, values_dir)
            if not os.path.exists(dir_path):
                shutil.copytree('../app/src/main/res/%s' % values_dir, dir_path)
                any_new_resources = True
    if any_new_resources:
        os.system("cd %s \
            && git pull \
            && git add . \
            && git commit -m \"feat: add %s language resources\" \
            && git push" % (app_language_dir, version_name))

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
    # info = _build_apk(BitConfiguration.BIT_64, FlavorConfiguration.OVERSEA)
    _copy_language_resources(info.version_name)
    gen_git_log(info)
    add_new_tag(info)
