#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from files import *
from apktool import *
from global_config import *

def assemble(is32Bit: bool) -> ApkInfo:
    '''Assemble the APK with given bit.''' 
    # Aassemble and copy to destination. 
    _do_real_assemble(is32Bit)
    info = _find_apk_under_given_directory(config.apk_output_dir)
    info.is32Bit = is32Bit
    _copy_apk_from_dir_to_dir(info, is32Bit, config.apk_copy_to)
    # Return the final APK info. 
    return info

def _do_real_assemble(is32Bit: bool):
    '''Do real assemble task.'''
    content = read_file(config.build_file)
    if is32Bit:
        content = _change_ndk_abi_filters(content, config.abi_filters_64, config.abi_filters_32)
    else:
        content = _change_ndk_abi_filters(content, config.abi_filters_32, config.abi_filters_64)
    write_file(config.build_file, content)
    os.system("cd %s && gradlew clean resguardProdRelease" % config.gradlew_dir)

def _change_ndk_abi_filters(content: str, f: str, t: str) -> str:
    '''Change nkd abi filters.'''
    return content.replace(f, t)

def _find_apk_under_given_directory(dir: str) -> ApkInfo:
    '''Get destination directory name.'''
    apk_parser = ApkParser()
    files = os.listdir(dir)
    for f in files:
        if f.endswith('apk'):
            path = os.path.join(dir, f)
            return apk_parser.get_apk_info(path)

def _copy_apk_from_dir_to_dir(info: ApkInfo, is32Bit: bool, td: str):
    '''Copy APK from one directory to another.'''
    if not info.is_valid():
        logging.error("The APK info is invalid.")
        return
    dir = os.path.join(td,  '%s_%s' % (info.vname, info.vcode) )
    if not os.path.exists(dir):
        os.mkdir(dir)
    fname = os.path.basename(info.path)
    prefix = info.get_file_prefix()
    fname = fname.replace(info.pkg, prefix)
    dest_path = os.path.join(dir, fname)
    copy_to(info.path, dest_path)
    # Fill in APk info.
    info.dest_dir = dir
    info.dest_path = dest_path
