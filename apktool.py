#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, os
import zipfile, traceback
import xml.dom.minidom
from global_config import *

class ApkInfo:

    def __init__(self, \
        source_apk_file_path: str = '', \
        package: str = '', \
        version_name: str = '', \
        version_code: str = ''
    ) -> None:
        '''
        The APK info.
        - source_apk_file_path: source apk path
        - package: package name
        - version_name: app version name
        - version_code: app version code
        '''
        self.source_apk_file_path = source_apk_file_path
        self.package = package
        self.version_code = version_code
        self.version_name = version_name
        self.build_bit:BitConfiguration = None
        self.build_flavor: FlavorConfiguration = None
        self.output_apk_directory = ''
        self.output_apk_file_path = ''

    def is_valid(self) -> bool:
        '''Is given APKInfo valid.'''
        return len(self.source_apk_file_path) > 0

    def __str__(self) -> str:
        return "ApkInfo([%s][%s][%s][%s])" % (self.source_apk_file_path, self.package, self.version_name, self.version_code)

def parse_apk_info(apk_file_path: str) -> ApkInfo:
    '''
    Parse APK info.
    - apk_file_path: path of APK file.
    '''
    logging.info("Trying to get apk info from [%s]" % apk_file_path)
    zipFile = zipfile.ZipFile(apk_file_path)
    zipFile.extract("AndroidManifest.xml", '.')
    zipFile.close()
    # out = os.popen("java -jar ../bin/AXMLPrinter.jar %s" % ('AndroidManifest.xml')).read().strip()
    out = os.popen("java -jar bin/AXMLPrinter.jar %s" % ('AndroidManifest.xml')).read().strip()
    try:
        root = xml.dom.minidom.parseString(out)
        collection = root.documentElement
        vcode = collection.getAttribute('android:versionCode')
        vname = collection.getAttribute('android:versionName')
        pkg = collection.getAttribute('package')
        return ApkInfo(apk_file_path, pkg, vname, vcode)
    except Exception:
        logging.error("Failed to parse Android manifest: %s" % traceback.format_exc())
    finally:
        os.remove('AndroidManifest.xml')
    return ApkInfo()
