#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, logging
from assemble import assemble
from diffuse import diff_apk
from files import *
from apktool import ApkInfo
from logger import config_logging
from gittag import gen_git_tag
from global_config import *

def _assemble_internal(is32Bit: bool) -> ApkInfo:
    '''Assemble APK and others.'''
    # Assemble APKs. 
    info = assemble(is32Bit)
    # Diff APKs or show APK info. 
    diff_apk(info)
    # Copy mapping file to destination. 
    mapping_to = os.path.join(info.dest_dir, "%s_mapping.txt" % info.get_file_prefix())
    copy_to(config.mapping_path, mapping_to)
    return info

def _copy_language_resources(version_name: str):
    '''Copy language resources to community repo and push to github.'''
    app_language_dir = os.path.join(config.languages_dir, version_name)
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

def _add_tag_automatically(version_name: str):
    '''Add tag for current commit.'''
    os.system("cd .. \
        && git add build.gradle \
        && git commit -m \"publish %s\" \
        && git push \
        && git tag v%s \
        && git push origin --tags" % (version_name, version_name))

if __name__ == "__main__":
    config_logging()
    config.parse()
    _assemble_internal(False)
    info = _assemble_internal(True)
    _add_tag_automatically(info.vname)
    _copy_language_resources(info.vname)
    gen_git_tag(info)
