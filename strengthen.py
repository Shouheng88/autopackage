#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from global_config import *
from logger import config_logging

def jiagu_360(apk_file_path: str, output_directory: str):
    '''Reinforce the APP.'''
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    os.system("java -jar %s -login %s %s\
        && java -jar %s -jiagu %s %s -autosign -automulpkg"\
        % (config.strengthen_jiagu_360_executor_path\
            , config.strengthen_jiagu_360_account\
            , config.strengthen_jiagu_360_password\
            , config.strengthen_jiagu_360_executor_path\
            , apk_file_path\
            , output_directory
        )
    )

if __name__ == "__main__":
    config_logging()
    config.parse()
    apk_path = "D:\\codes\\other\\LeafNote-resources\\apks\\3.5.1_261\\32BIT-prod-release-3.5.1-261.apk"
    out_dir = "D:\\codes\\other\\LeafNote-resources\\apks\\3.5.1_261"
    jiagu_360(apk_path, out_dir)
    # info = os.stat()
    # print(info.st_atime)
