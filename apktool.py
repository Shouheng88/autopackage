#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, os
import zipfile, traceback
import xml.dom.minidom

class ApkInfo:

    def __init__(self, path: str = '', pkg: str = '', vname: str = '', vcode: str = '') -> None:
        '''
        The APK info.
        - path: apk path
        - pkg: package name
        - vname: app version name
        - vcode: app version code
        '''
        self.path = path
        self.pkg = pkg
        self.vcode = vcode
        self.vname = vname

    def is_valid(self) -> bool:
        '''Is given APKInfo valid.'''
        return len(self.path) > 0

    def __str__(self) -> str:
        return "ApkInfo([%s][%s][%s][%s])" % (self.path, self.pkg, self.vname, self.vcode)

class ApkParser:
    
    def get_apk_info(self, path: str) -> ApkInfo:
        '''
        Get APK info.
        - path: path of APK file.
        '''
        logging.info("Trying to get apk info from [%s]" % path)
        zipFile = zipfile.ZipFile(path)
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
            return ApkInfo(path, pkg, vname, vcode)
        except Exception:
            logging.error("Failed to parse Android manifest: %s" % traceback.format_exc())
        finally:
            os.remove('AndroidManifest.xml')
        return ApkInfo()
