#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil, os
from logger import *
from global_config import *
from pathlib import Path

ORIGINAL_COPY_TO_DIRECTORY_NAME = "original"
ORIGINAL_COPY_TO_INFO_FILE_NAME = ".info"

def copy_language_resources(version_name: str):
    '''Copy language resources to community repo and push to github.'''
    _copy_origin_language_resources(version_name)
    _compare_language_resources(version_name)

def _compare_language_resources(version_name: str):
    '''Compare current language resources with last version.'''
    resoueces_directory = '%sapp/src/main/res/' % config.gradlew_location
    app_language_directory = os.path.join(config.output_languages_directory, ORIGINAL_COPY_TO_DIRECTORY_NAME)
    copy_to_info_file_path = os.path.join(app_language_directory, ORIGINAL_COPY_TO_INFO_FILE_NAME)
    last_version = read_file(copy_to_info_file_path).strip()
    diff_directory_name = "diff_%s_to_%s" % (last_version, version_name)
    diff_directory_path = os.path.join(config.output_languages_directory, diff_directory_name)
    for name in os.listdir(app_language_directory):
        path = os.path.join(app_language_directory, name)
        if Path(path).is_dir:
            # Compare in the child directory. Here we only compare two level directories!
            for child_name in os.listdir(path):
                sub_file_path = os.path.join(path, child_name)
                if Path(sub_file_path).is_file and name.endswith('.xml'):
                    compare_from = sub_file_path
                    compare_to = os.path.join(resoueces_directory, name, child_name)
                    write_to = os.path.join(diff_directory_path, name, child_name)
                    _compare_language_resource_file_and_output(compare_from, compare_to, write_to)
        elif Path(path).is_file and name.endswith('.xml'):
            compare_from = path
            compare_to = os.path.join(resoueces_directory, name)
            write_to = os.path.join(diff_directory_path, name)
            _compare_language_resource_file_and_output(compare_from, compare_to, write_to)

def _compare_language_resource_file_and_output(compare_from: str, compare_to: str, write_to: str):
    '''Compare language resource file and output the diff result.'''
    pass

def _copy_origin_language_resources(version_name: str):
    '''Copy origin language resources.'''
    app_language_directory = os.path.join(config.output_languages_directory, ORIGINAL_COPY_TO_DIRECTORY_NAME)
    any_new_resources = False
    resoueces_directory = '%sapp/src/main/res/' % config.gradlew_location
    if not os.path.exists(resoueces_directory):
        loge("Resources directory doesn't exist or not match 'app/src/main/res/' pattern.")
        return
    for name in os.listdir(resoueces_directory):
        if name.startswith('values'):
            copy_from_directory = os.path.join(resoueces_directory, name)
            copy_to_directory = os.path.join(app_language_directory, name)
            if not os.path.exists(copy_to_directory) and Path(copy_from_directory).is_dir:
                # Delete the copy to directory if it exists before make a copy!
                if os.path.exists(copy_to_directory):
                    shutil.rmtree(copy_to_directory)
                shutil.copytree(copy_from_directory, copy_to_directory)
                any_new_resources = True
    if any_new_resources:
        copy_to_info_file_path = os.path.join(app_language_directory, ORIGINAL_COPY_TO_INFO_FILE_NAME)
        write_file(copy_to_info_file_path, version_name)
        os.system("cd %s \
            && git pull \
            && git add . \
            && git commit -m \"feat: version %s language resources\" \
            && git push" % (app_language_directory, version_name))

if __name__ == "__main__":
    config_logging()
