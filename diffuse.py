#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from apktool import *
from files import *
from global_config import *

def diff_apk(info: ApkInfo) -> str:
    '''Diff APK or output its information.'''
    apk_output_dir = config.apk_copy_to
    last_version_dir = _find_last_apk_version(info, apk_output_dir)
    logging.debug("Found last version dir: %s" % last_version_dir)
    if len(last_version_dir) == 0:
        return _output_apk_info(info)
    else:
        return _output_apk_diff(info, last_version_dir)

def _find_last_apk_version(info: ApkInfo, output_dir: str) -> str:
    '''Find last APK version by directory name.'''
    last_version = 0
    last_version_dir = ''
    for dir in os.listdir(output_dir):
        parts = dir.split('_')
        if len(parts) > 1:
            vcode = parts[1]
            if not info.vcode == vcode and int(vcode) > last_version:
                last_version = int(vcode)
                last_version_dir = dir
    return os.path.join(output_dir, last_version_dir)

def _output_apk_info(info: ApkInfo) -> str:
    '''Output the APK info.'''
    content = os.popen("java -jar bin/diffuse.jar info %s" % info.dest_path).read().strip()
    fname = os.path.join(info.dest_dir, "%s_info.txt" % info.get_file_prefix())
    write_file(fname, content)
    return content

def _get_last_apk_path(info: ApkInfo, last_version_dir: str) -> str:
    '''Get last APK file path.'''
    for f in os.listdir(last_version_dir):
        if (f.startswith("32BIT") and f.endswith(".apk") and info.is32Bit) \
            or (f.startswith('64BIT') and f.endswith(".apk") and not info.is32Bit):
            return os.path.join(last_version_dir, f)
    return ''

def _output_apk_diff(info: ApkInfo, last_version_dir: str) -> str:
    '''Output the APK info.'''
    last_apk_path = _get_last_apk_path(info, last_version_dir)
    if len(last_apk_path) == 0:
        _output_apk_info(info)
        return
    content = os.popen("java -jar bin/diffuse.jar diff %s %s" % (last_apk_path, info.dest_path)).read().strip()
    fname = os.path.join(info.dest_dir, "%s_diff.txt" % info.get_file_prefix())
    write_file(fname, content)
    return content
