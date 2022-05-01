#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

def config_logging(filename: str = 'app.log'):
    '''Config logging library globaly.'''
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename=filename, filemode='a', level=logging.DEBUG, format=log_format, datefmt=date_format)
    logging.FileHandler(filename=filename, encoding='utf-8')
