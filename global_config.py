#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logger import *
from files import *
from enum import Enum
from typing import Dict

YAML_CONFIGURATION_FILE_PATH = "config/config.yml"

class BuildConfiguration:
    '''Build Environment Configuration.'''
    def __init__(self):
        # Build target script
        self.target_script = YAML_CONFIGURATION_FILE_PATH
        # Build APK version name
        self.version_name = ''
        # Build APK version code
        self.version_code = ''
        
class BitConfiguration(Enum):
    '''Assemble APK package bit configuration, namely, 32 bit, 64 bit and 64 + 32 bit packages.'''
    BIT_32 = 0
    BIT_64 = 1
    BIT_32_64 = 2

    def get_name(self) -> str:
        '''Get bit configuration name.'''
        if self == BitConfiguration.BIT_32:
            return 'ndk_32'
        elif self == BitConfiguration.BIT_32_64:
            return 'ndk_32_64'
        else:
            return 'ndk_64'

    def get_gradlew_bit_param_value(self) -> str:
        '''Get gradlew build parameter for given ndk/bit configuration.'''
        if self == BitConfiguration.BIT_32:
            return 'ndk_32'
        elif self == BitConfiguration.BIT_32_64:
            return 'ndk_32_64'
        else:
            return 'ndk_64'

class FlavorConfiguration(Enum):
    '''Assemble APK package flavor configuration, namely, national and international packages.'''
    NATIONAL = 0
    OVERSEA = 1

    def get_name(self) -> str:
        '''Get flavor name.'''
        if self == FlavorConfiguration.OVERSEA:
            return "oversea"
        return "national"

    def get_gradlew_command(self) -> str:
        '''Get gradlew command configuration base on current flavor.'''
        if self == FlavorConfiguration.OVERSEA:
            return config._assemble_command_oversea
        return config._assemble_command_national

    def get_apk_output_directory(self) -> str:
        '''Get APK output directory base on current flavor.'''
        if self == FlavorConfiguration.OVERSEA:
            return config._apk_output_directory_oversea
        return config._apk_output_directory_national

class GlobalConfig:
    def parse(self):
        self._configurations = read_yaml(build_config.target_script)
        logd(str(self._configurations))
        # Gradlew Build Configurations.
        self.gradlew_location = self._read_key("build.gradlew_location")
        self._assemble_command_national = self._read_key("build.assemble_command.national")
        self._assemble_command_oversea  = self._read_key("build.assemble_command.oversea")
        self._apk_output_directory_national = self._read_key('build.apk_output_directory.national')
        self._apk_output_directory_oversea  = self._read_key('build.apk_output_directory.oversea')
        self.mapping_file_path = self._read_key("build.mapping_file_path")
        self.gradle_java_home = self._read_key("build.gradle_java_home")
        # APK Strength Configurations.
        self.strengthen_enable = self._read_key('strengthen.enable')
        self.strengthen_jiagu_360_executor_path = self._read_key('strengthen.jiagu_360.executor_path')
        self.strengthen_jiagu_360_account = self._read_key('strengthen.jiagu_360.account')
        self.strengthen_jiagu_360_password = self._read_key('strengthen.jiagu_360.password')
        # Final Output Configurations.
        self.output_apk_directory = self._read_key('output.apk_directory')
        self.output_languages_directory = self._read_key('output.languages_directory')
        self.output_mail_title = self._read_key('output.mail.title')
        self.output_mail_receivers = self._read_key('output.mail.receivers')
        self.output_mail_user = self._read_key('output.mail.user')
        self.output_mail_password = self._read_key('output.mail.password')
        self.output_gitlog_store_file = self._read_key('output.git_log_store_file')
        # APK Publish Configurations.
        self.publish_lanzou_username = self._read_key('publish.lanzou.username')
        self.publish_lanzou_password = self._read_key('publish.lanzou.password')
        self.publish_lanzou_ylogin = self._read_key('publish.lanzou.ylogin')
        self.publish_lanzou_phpdisk_info = self._read_key('publish.lanzou.phpdisk_info')
        self.publish_telegram_chat_id = self._read_key('publish.telegram.chat_id')
        self.publish_telegram_token = self._read_key('publish.telegram.token')

    def _read_key(self, key: str):
        '''Read key from configurations.'''
        parts = key.split('.')
        value = self._configurations
        for part in parts:
            value = value[part.strip()]
        return value

# Global Build Configuration.
build_config = BuildConfiguration()

# Global Configuration From Target Script. 
config = GlobalConfig()

if __name__ == "__main__":
    config_logging()
    print(config._assemble_command_national)
    print(config.output_mail_receivers)
