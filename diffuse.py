#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from apktool import *
from files import *
from global_config import *

DIFF_RESULT_HTML_TEMPLATE = "config/template_diff.html"
DIFF_RESULT_HTML_PLACEHOLER = "diff_result_content"

def diff_apk(info: ApkInfo) -> str:
    '''Diff APK or output its information.'''
    last_version_directory = _find_last_version_directory(info)
    logd("Found last version directory: %s" % last_version_directory)
    diff_result = ''
    if len(last_version_directory) == 0:
        diff_result = _output_current_apk_information(info)
    else:
        diff_result = _output_apk_diff_result(info, last_version_directory)
    # Format diff result as a html content.
    html_diff_content = read_file(DIFF_RESULT_HTML_TEMPLATE)
    html_diff_content = html_diff_content.replace(DIFF_RESULT_HTML_PLACEHOLER, diff_result)
    return html_diff_content

def _find_last_version_directory(info: ApkInfo) -> str:
    '''Find last APK version by APK output directory.'''
    last_version = 0
    last_version_directory = ''
    output_apk_directory = config.output_apk_directory
    logd("finding last version under %s" % (output_apk_directory))
    for directory in os.listdir(output_apk_directory):
        logd("finding last version under %s" % (directory))
        directory_parts = directory.split('_')
        if directory != ".DS_Store" and len(directory_parts) > 1:
            version_code = directory_parts[1]
            if not info.version_code == version_code and int(version_code) > last_version:
                last_version = int(version_code)
                last_version_directory = directory
    if len(last_version_directory) == 0:
        return ''
    return os.path.join(output_apk_directory, last_version_directory)

def _output_current_apk_information(info: ApkInfo) -> str:
    '''Output current APK information.'''
    diff_result_content = os.popen("java -jar bin/diffuse.jar info %s" % info.output_apk_file_path).read().strip()
    diff_result_file_name = os.path.join(info.output_apk_directory, \
        "diff_result_%s_%s_info.txt" % (info.build_flavor.get_name(), info.build_bit.get_name()))
    write_file(diff_result_file_name, diff_result_content)
    return diff_result_content

def _get_last_version_apk_file_path(info: ApkInfo, last_version_directory: str) -> str:
    '''Get last version APK file path.'''
    bit_name = info.build_bit.get_name()
    flavor_name = info.build_flavor.get_name()
    for file_name in os.listdir(last_version_directory):
        if file_name.endswith(".apk") and file_name.find(bit_name) >= 0 and file_name.find(flavor_name) >= 0:
            return os.path.join(last_version_directory, file_name)
    return ''

def _output_apk_diff_result(info: ApkInfo, last_version_directory: str) -> str:
    '''Output APKs diff result.'''
    last_version_apk_file_path = _get_last_version_apk_file_path(info, last_version_directory)
    if len(last_version_apk_file_path) == 0:
        logi("Last version APK file not found!")
        return _output_current_apk_information(info)
    logi("Found last version APK file: %s" % last_version_apk_file_path)
    diff_result_content = os.popen("java -jar bin/diffuse.jar diff %s %s" % \
        (last_version_apk_file_path, info.output_apk_file_path)).read().strip()
    diff_result_file_name = os.path.join(info.output_apk_directory, \
        "diff_result_%s_%s_info.txt" % (info.build_flavor.get_name(), info.build_bit.get_name()))
    write_file(diff_result_file_name, diff_result_content)
    return diff_result_content
