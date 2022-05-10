#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, os, urllib, random, requests
from apktool import *
from files import *
from global_config import *
from logger import config_logging
from typing import List
from requests_toolbelt.multipart.encoder import MultipartEncoder

fileup_url = r'http://up.woozooo.com/fileup.php'

def upload(name: str, path: str):
    '''Upload file to lanzou cloud.'''
    logging.info("Uploading to lanzou cloud: %s" % f)
    name = urllib.parse.quote(name)
    fileup_headers = {
        "Accept": "* / *",
        "Accept - Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Origin": "https://up.woozooo.com",
        "Referer": "https://up.woozooo.com/mydisk.php?item=files&action=index",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    multipart_encoder = MultipartEncoder(
        fields={
            "task": "1",
            "folder_id": "-1",
            "id": "WU_FILE_0",
            "name": f,
            "type": "application/octet-stream",
            # "lastModifiedDate": "Thu Jun 27 2019 12:11:16 GMT 0800 (中国标准时间)",
            # "size": "185",
            'upload_file': (name, open(path, 'rb'), 'application/octet-stream')
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    fileup_headers['Content-Type'] = multipart_encoder.content_type
    fileup_json = session.post(url = fileup_url, data=multipart_encoder, headers=fileup_headers).json()
    if fileup_json['zt'] == 1:
        logging.inf("Succeed to upload: %s" % name)
    return fileup_json

def a_upload(name: str, path: str):
    '''
    - ylogin: the ylogin cookie from lanzou cloud, get cookie from 'chrome dev tools -> security -> cookie' 
    - name: file name should have the extension info, and it should be supported your lanzou cloud account
    - path: the file path to upload
    '''
    if len(config.lanzou_ylogin) == 0:
        logging.error("lanzou cloud ylogin filed required!")
        return
    if len(config.lanzou_phpdisk_info) == 0:
        logging.error("lanzou cloud phpdisk_info filed required!")
        return
    url_upload = "https://up.woozooo.com/fileup.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': f'https://up.woozooo.com/mydisk.php?item=files&action=index&u={config.lanzou_ylogin}'
    }
    post_data = {
        "task": "1",
        "folder_id": "-1",
        "id": "WU_FILE_0",
        "name": name,
    }
    cookie = {
        'ylogin': config.lanzou_ylogin,
        'phpdisk_info': config.lanzou_phpdisk_info
    }
    files = {'upload_file': (name, open(path, "rb"), 'application/octet-stream')}
    multipart_encoder = MultipartEncoder(
        fields={
            "task": "1",
            "folder_id": "-1",
            "id": "WU_FILE_0",
            "name": name,
            "type": "application/octet-stream",
            # "lastModifiedDate": "Thu Jun 27 2019 12:11:16 GMT 0800 (中国标准时间)",
            # "size": "185",
            'upload_file': (name, open(path, 'rb'), 'application/octet-stream')
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    # headers['Content-Type'] = multipart_encoder.content_type
    # res = requests.post(url_upload, data=post_data, headers=headers, cookies=cookie, timeout=120).json()
    res = requests.post(url_upload, data=post_data, files=files, headers=headers, cookies=cookie, timeout=120).json()
    # res = requests.session().post(url = fileup_url, data=multipart_encoder, headers=headers).json()
    logging.info(res)
    return res['zt'] == 1

def login(username: str, passed: str):
    '''Log in lanzou cloud.'''
    session = requests.session()
    
    login_url = r'https://up.woozooo.com/account.php'
    
    login_data = {
        "action": "login",
        "task": "login",
        "ref": "https://up.woozooo.com/",
        "formhash": "0af1aa15",
        "username": username,
        "password": passed,
    }

    mydisk_data = {
        "task": "5",
        "folder_id": "-1",
        "pg": "1",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    login_json = session.post(url=login_url, data=login_data, headers=headers).text
    return login_json

def a_login(ylogin: str, phpdisk_info: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://pc.woozooo.com/account.php?action=login'
    }
    cookie = {
        'ylogin': ylogin,
        'phpdisk_info': phpdisk_info
    }
    url_account = "https://pc.woozooo.com/account.php"
    if cookie['phpdisk_info'] is None:
        logging.error('ERROR: phpdisk_info in Cookie is required!')
        return False
    if cookie['ylogin'] is None:
        logging.error('ERROR: ylogin in Cookie is required!')
        return False
    res = requests.get(url_account, headers=headers, cookies=cookie, verify=True)
    if '网盘用户登录' in res.text:
        log('ERROR: Failed to login lanzou cloud!')
        return False
    else:
        logging.info("Succeed to login lanzou cloud!")
        return True

if __name__ == "__main__":
    config_logging()
    config.parse()
    # ret = a_login(ylogin, phpdisk_info)
    # if ret:
    ret = a_upload("test2.apk", "D:\\codes\\other\\LeafNote-resources\\apks\\3.5.1_261\\32BIT-prod-release-3.5.1-261.apk")
    print(ret)
