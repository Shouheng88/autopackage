#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from logger import *

def generate_apk_channels(apk_path: str, channels: [str], output_dir):
    '''Generate APK with channels.'''
    if len(channels) == 0:
        logi('No channels to generate, ignored ...')
        return True
    channels_str = ','.join(channels)
    os.popen("java -jar bin/VasDolly.jar put -c \"%s\" %s %s" % (channels_str, apk_path, output_dir)).read().strip()
