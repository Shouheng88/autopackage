#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from global_config import *
from logger import *
from telegram_bot import send_apk
from lanzou import a_upload
from files import *
from git_tag import COMMUNITY_LOGS_DIR

def publish(app: str, ver: str):
    '''
    Publish APKs.
    - app: APP name
    - ver: the version of APKs to publish
    '''
    if ver is None or len(ver) == 0:
        loge("Failed: version code is invalid!")
        return
    dest_dir = ''
    for dir in os.listdir(config.output_apk_directory):
        if dir.startswith(ver + "_"):
            dest_dir = os.path.join(config.output_apk_directory, dir)
            break
    if len(dest_dir) == 0:
        loge("Failed to find APK of version: [%s]" % ver)
        return
    found_tg = 0
    found_lz = 0
    channels_dir = dest_dir + '/channels'
    for apk in os.listdir(channels_dir):
        if apk.endswith(".apk") and apk.find("telegram") != -1:
            found_tg = found_tg + 1
            path = os.path.join(channels_dir, apk)
            _publish_to_tg(app, path, ver)
        elif apk.endswith(".apk") and apk.find("lanzou") != -1:
            found_lz = found_lz + 1
            path = os.path.join(channels_dir, apk)
            _publish_to_lanzou(path, ver)
    logi("Published APKs for tG: %d" % (found_tg))
    logi("Published APKs for Lanzou cloud: %d" % (found_lz))

def _publish_to_tg(app: str, apk: str, ver:str):
    '''Publish APK to TG.'''
    logd("Publishing [%s] to TG." % (apk))
    msg = 'Hello friends! There\'s a new version [%s] of our %s for %s!\n'
    suffix = ''
    if apk.find("32BIT") != -1:
        suffix = '32bit'
        msg = msg % (ver, app, '32 bit')
    else:
        suffix = '64bit'
        msg = msg % (ver, app, '64 bit')
    upgrade_log = _read_upgrade_log(ver)
    if upgrade_log is None or len(upgrade_log) > 0:
        msg = msg + "\nUpgrade log (auto generated):\n" + upgrade_log
    msg = msg + "\n\nThis message is send by bot. If you have any questions, please contact the admin for help :P"
    send_apk(apk, "%s_v%s_%s.apk" % (app, ver, suffix), msg)

def _publish_to_lanzou(apk: str, ver:str):
    '''Publish APK to Lanzou cloud.'''
    logd("Publishing %s to LZ." % (apk))
    name = os.path.basename(apk)
    a_upload(name, apk)

def _read_upgrade_log(ver: str) -> str:
    '''Read upgrade log generated!'''
    path = COMMUNITY_LOGS_DIR + "/" + ver + ".txt"
    if not os.path.exists(path):
        loge("Upgrade log not found: [%s]!" % path)
        return
    return read_file(path)

if __name__ == "__main__":
    '''Test entry.'''
    config_logging()
    # print(_read_upgrade_log("3.5"))
    publish("LeafNote", "3.5")
