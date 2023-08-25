#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from files import *
from apktool import *
from global_config import *
from logger import *
from channel import *

def assemble(bit: BitConfiguration, flavor: FlavorConfiguration) -> ApkInfo:
    '''Assemble APK with bit and flavor and copy APK and mapping files to destination.''' 
    # ./gradlew assembleNationalDebug -Pbuild_ndk_type=ndk_32 -Pversion_name=3.8.0
    assemble_command = "cd %s && gradlew clean %s -Pbuild_ndk_type=%s" \
        % (config.gradlew_location, flavor.get_gradlew_command(), bit.get_gradlew_bit_param_value())
    if  len(config.gradle_java_home) > 0:
        assemble_command = assemble_command + (" -Dorg.gradle.java.home=\"%s\"" % config.gradle_java_home)
    if len(build_config.version) != 0:
        assemble_command = assemble_command + " -Pversion_name=" + build_config.version
    logi("Final gradlew command is [%s]" % assemble_command)
    os.system(assemble_command)
    info = _find_apk_under_given_directory(bit, flavor)
    _copy_apk_to_directory(info)
    _copy_mapping_file_to_directory(info, flavor)
    _package_apk_channels(info)
    return info

def _find_apk_under_given_directory(bit: BitConfiguration, flavor: FlavorConfiguration) -> ApkInfo:
    '''Get destination directory name.'''
    apk_output_directory = flavor.get_apk_output_directory()
    files = os.listdir(apk_output_directory)
    for f in files:
        if f.endswith('apk'):
            path = os.path.join(apk_output_directory, f)
            info = parse_apk_info(path)
            break
    # Fill bit and flavor configuration.
    if info is not None:
        info.build_bit = bit
        info.build_flavor = flavor
    return info

def _copy_apk_to_directory(info: ApkInfo):
    '''Copy APK from one directory to another.'''
    if not info.is_valid():
        loge("The APK info is invalid.")
        return
    output_apk_directory = os.path.join(config.output_apk_directory, '%s_%s' % (info.version_name, info.version_code))
    if not os.path.exists(output_apk_directory):
        os.mkdir(output_apk_directory)
    apk_file_base_name = os.path.basename(info.source_apk_file_path)
    output_apk_file_path = os.path.join(output_apk_directory, apk_file_base_name)
    copy_to(info.source_apk_file_path, output_apk_file_path)
    # Fill in APk info.
    info.output_apk_directory = output_apk_directory
    info.output_apk_file_path = output_apk_file_path

def _copy_mapping_file_to_directory(info: ApkInfo, flavor: FlavorConfiguration):
    '''Copy mapping file to given directory.'''
    mapping_file_name = "%s_mapping.txt" % flavor.get_name()
    mapping_file_copy_to = os.path.join(info.output_apk_directory, mapping_file_name)
    copy_to(config.mapping_file_path, mapping_file_copy_to)

def _package_apk_channels(info: ApkInfo):
    '''Package App with different channels.'''
    generate_apk_channels(info.source_apk_file_path, config.output_channels, config.output_apk_directory)
