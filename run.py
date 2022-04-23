#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, logging
from assemble import assemble
from diffuse import diff_apk
from files import *
from apktool import ApkInfo

# The path under witch to find the APKs. 
PROD_OUTPUT_APK_PATH = ""
# The mapping file location. 
MAPPING_FILE_PATH = "../app/mapping.txt"
# The directory to store the assembled APKs. 
FINAL_OUTPUT_DIRECTORY = ""
# The directory to store the languages files. 
COMMUNITY_LANGUAGES_DIR = "D:/codes/other/LeafNote-Community/languages/app"

def _config_logging(filename: str = 'app.log'):
    '''Config logging library globaly.'''
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format=log_format, datefmt=date_format)
    logging.FileHandler(filename=filename, encoding='utf-8')

def _assemble_internal(is32Bit: bool) -> ApkInfo:
    '''Assemble APK and others.'''
    # Assemble APKs. 
    info = assemble(is32Bit)
    # Diff APKs or show APK info. 
    diff_apk(info)
    # Copy mapping file to destination. 
    mapping_to = os.path.join(info.dest_dir, "%s_mapping.txt" % info.get_file_prefix())
    copy_to(MAPPING_FILE_PATH, mapping_to)
    return info

def _copy_language_resources(version_name: str):
    '''Copy language resources to community repo and push to github.'''
    app_language_dir = os.path.join(COMMUNITY_LANGUAGES_DIR, version_name)
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
    os.system("git add ../build.gradle \
        && git commit -m \"publish %s\" \
        && git push \
        && git tag v%s \
        && git push origin --tags" % (version_name, version_name))

if __name__ == "__main__":
    _config_logging()
    _assemble_internal(True)
    info = _assemble_internal(False)
    _add_tag_automatically(info.vname)
    _copy_language_resources(info.vname)
