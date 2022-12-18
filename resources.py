#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil, os
from logger import *
from global_config import *
from pathlib import Path
from files import parse_xml

ORIGINAL_COPY_TO_DIRECTORY_NAME = "original"
ORIGINAL_COPY_TO_INFO_FILE_NAME = ".info"

def copy_language_resources(version_name: str):
    '''Copy language resources to community repo and push to github.'''
    # Compare and then copy language resources.
    _compare_language_resources(version_name)
    _copy_origin_language_resources(version_name)

def _compare_language_resources(version_name: str):
    '''Compare current language resources with last version.'''
    resoueces_directory = '%sapp/src/main/res/' % config.gradlew_location
    copied_language_directory = os.path.join(config.output_languages_directory, ORIGINAL_COPY_TO_DIRECTORY_NAME)
    copied_to_info_file_path = os.path.join(copied_language_directory, ORIGINAL_COPY_TO_INFO_FILE_NAME)
    last_version = read_file(copied_to_info_file_path).strip()
    diff_directory_name = "diff_%s_to_%s.txt" % (last_version, version_name)
    diff_directory_path = os.path.join(config.output_languages_directory, diff_directory_name)
    for resource_file_name in os.listdir(resoueces_directory):
        resource_file_path = os.path.join(resoueces_directory, resource_file_name)
        if Path(resource_file_path).is_dir():
            # Compare in the child directory. Here we only compare two level directories!
            resource_directory_path = resource_file_path
            for resource_child_file_name in os.listdir(resource_directory_path):
                resource_child_file_path = os.path.join(resource_directory_path, resource_child_file_name)
                if Path(resource_child_file_path).is_file() and resource_child_file_name.endswith('.xml'):
                    compare_from = resource_child_file_path
                    compare_to = os.path.join(copied_language_directory, resource_file_name, resource_child_file_name)
                    write_to = os.path.join(diff_directory_path, resource_file_name, resource_child_file_name)
                    _compare_language_resource_file_and_output(compare_from, compare_to, write_to)
        elif Path(resource_file_path).is_file() and resource_file_name.endswith('.xml'):
            compare_from = resource_file_path
            compare_to = os.path.join(copied_language_directory, resource_file_name)
            write_to = os.path.join(diff_directory_path, resource_file_name)
            _compare_language_resource_file_and_output(compare_from, compare_to, write_to)

def _compare_language_resource_file_and_output(compare_from: str, compare_to: str, write_to: str):
    '''Compare language resource file and output the diff result.'''
    if not os.path.exists(compare_to):
        copy_to(compare_from, write_to)
        return
    from_dict = parse_xml(compare_from)
    to_dict = parse_xml(compare_to)
    compare_result: Dict[str, List[str]] = {}
    # Make a diff between string resources and old resources.
    for name, value in from_dict.items():
        if name not in to_dict or "\n".join(value) != "\n".join(to_dict[name]):
            compare_result[name] = value
    # Build compare result file content and write to file.
    if len(compare_result) > 0:
        comapre_content = ''
        for name, value in compare_result.items():
            comapre_content += ('=== name:\n' + name + "\n")
            comapre_content += ('=== value:\n' + "\n".join(value) + "\n\n")
    write_file(write_file, comapre_content)

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
            if Path(copy_from_directory).is_dir():
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
