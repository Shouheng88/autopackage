#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil, logging, getopt, sys
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

command_info = "\
Options: \n\
    -h[--help]                 Help info\n\
    -c[--script]               Target build script path\n\
    -e[--version_name]         Build APK version name\n\
    -s[--version_code]         Build APK version code"

def _build_apk(bit: BitConfiguration, flavor: FlavorConfiguration) -> ApkInfo:
    '''Execute APK build flow.'''
    info = assemble(bit, flavor)
    diff = diff_apk(info)
    jiagu_file_directory = os.path.join(info.output_apk_directory, 'strengthen')
    jiagu_360(info.output_apk_file_path, jiagu_file_directory)
    mail_subject = "%s(%s,%s)" % (config.output_mail_title, flavor.get_name(), bit.get_name())
    send_email(config.output_mail_receivers, mail_subject, diff, 'html')
    return info

def _show_invalid_command(info: str):
    '''Show command invalid info.'''
    print('Error: Unrecognized command: %s' % info)
    print(command_info)     

def _parse_command(argv):
    '''Parse command.'''
    try:
        opts, args = getopt.getopt(argv, "-h:-s:-n:-v:", ["help", "script=", 'version_name=', 'version_code='])
    except BaseException as e:
        _show_invalid_command(str(e))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-s', '--script'):
            build_config.target_script = arg 
        elif opt in ('-n', '--version_name'):
            build_config.version_name = arg
        elif opt in ("-v", "--version_code"):
            build_config.version_code = arg
        elif opt in ('-h', '--help'):
            print(command_info)
    logi("Build Info: target script[%s], version name[%s] and version code[%s]" 
         % (build_config.target_script, build_config.version_name, build_config.version_code))

def _run_main():
    '''Run main program.'''
    info = _build_apk(BitConfiguration.BIT_64, FlavorConfiguration.NATIONAL)
    info = _build_apk(BitConfiguration.BIT_64, FlavorConfiguration.OVERSEA)
    copy_language_resources(info.version_name)
    gen_git_log(info)
    add_new_tag(info)

if __name__ == "__main__":
    ''' python run.py -s config/config_product.yml -v 324 -n 3.8.1.2 '''
    config_logging()
    _parse_command(sys.argv[1:])
    config.parse()
    _run_main()
