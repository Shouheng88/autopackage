#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

def config_logging(filename: str = 'app.log'):
    '''Config logging library globaly.'''
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format=log_format, datefmt=date_format)
    logging.FileHandler(filename=filename, encoding='utf-8')

def logd(msg: str):
    '''D level log.'''
    print(msg)
    logging.debug(msg)

def loge(msg: str):
    '''E level log.'''
    print(msg)
    logging.error(msg)(msg)
    
def logi(msg: str):
    '''I level log.'''
    print(msg)
    logging.info(msg)
