#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from files import *
from apktool import *

YAML_CONFIGURATION_FILE_PATH = "config.yml"

def assemble(is32Bit: bool) -> ApkInfo:
    '''Assemble the APK with given bit.''' 
    # Read configurations. 
    configurations = read_yaml(YAML_CONFIGURATION_FILE_PATH)
    logging.debug(str(configurations))
    build_file = configurations['build']['file']
    gradlew_dir = configurations['build']['gradlew']
    abi_filters_32 = configurations['build']['ndk']['abi_32']
    abi_filters_64 = configurations['build']['ndk']['abi_64']
    apk_output_dir = configurations['build']['apk_output_dir']
    apk_copy_to = configurations['dest']['apk_dir']
    # Aassemble and copy to destination. 
    _do_real_assemble(is32Bit, gradlew_dir, build_file, abi_filters_64, abi_filters_32)
    info = _find_apk_under_given_directory(apk_output_dir)
    _copy_apk_from_dir_to_dir(info, apk_copy_to)
    # Return the final APK info. 
    return info

def _do_real_assemble(is32Bit: bool, gradlew_dir: str, build_file: str, \
    abi_filters_64: str, abi_filters_32: str):
    '''Do real assemble task.'''
    content = read_file(build_file)
    if is32Bit:
        _change_ndk_abi_filters(content, abi_filters_64, abi_filters_32)
    else:
        _change_ndk_abi_filters(content, abi_filters_32, abi_filters_64)
    write_file(build_file, content)
    os.system("cd %s && gradlew clean resguardProdRelease" % gradlew_dir)

def _change_ndk_abi_filters(content: str, f: str, t: str) -> str:
    '''Change nkd abi filters.'''
    return content.replace(f, t)

def _find_apk_under_given_directory(dir: str) -> ApkInfo:
    '''Get destination directory name.'''
    apk_parser = ApkParser()
    files = os.listdir(dir)
    for f in files:
        if f.endswith('apk'):
            return apk_parser.get_apk_info(path)

def _copy_apk_from_dir_to_dir(info: ApkInfo, td: str):
    '''Copy APK from one directory to another.'''
    if not info.is_valid():
        logging.error("The APK info is invalid.")
        return
    vname = info.vname
    dir = os.path.join(td, vname)
    if not os.path.exists(dir):
        os.mkdir(dir)
    fname = os.path.basename(info.path)
    dest_path = os.path.join(dir, fname)
    copy_to(info.path, dest_path)
