#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from files import *

YAML_CONFIGURATION_FILE_PATH = "config.yml"

class GlobalConfig:
    def __init__(self):
        self.build_file = ''
        self.gradlew_dir = ''
        self.abi_filters_32 = ''
        self.abi_filters_64 = ''
        self.apk_output_dir = ''
        self.apk_copy_to = '' 

    def parse(self):
        '''Parse global configurations from config yaml file.'''
        configurations = read_yaml(YAML_CONFIGURATION_FILE_PATH)
        logging.debug(str(configurations))
        self.build_file = configurations['build']['file']
        self.gradlew_dir = configurations['build']['gradlew']
        self.abi_filters_32 = configurations['build']['ndk']['abi_32']
        self.abi_filters_64 = configurations['build']['ndk']['abi_64']
        self.apk_output_dir = configurations['build']['apk_output_dir']
        self.apk_copy_to = configurations['dest']['apk_dir']

config = GlobalConfig()
