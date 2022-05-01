#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, logging
from global_config import *
from logger import config_logging

def jiagu(apk: str, out: str):
    '''Reinforce the APP.'''
    os.system("java -jar %s -login %s %s\
        && java -jar %s -jiagu %s %s -autosign -automulpkg"\
        % (config.jiagu_exec_path, config.jiagu_account, config.jiagu_password\
            , config.jiagu_exec_path, apk, out))

if __name__ == "__main__":
    config_logging()
    config.parse()
    apk_path = "D:\\codes\\other\\LeafNote-resources\\apks\\3.5.1_261\\32BIT-prod-release-3.5.1-261.apk"
    out_dir = "D:\\codes\\other\\LeafNote-resources\\apks\\3.5.1_261"
    jiagu(apk_path, out_dir)
    # info = os.stat()
    # print(info.st_atime)
