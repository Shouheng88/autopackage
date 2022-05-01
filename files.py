#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os, yaml, logging, traceback, shutil

def read_yaml(yaml_file: str):
    '''Read YAML.'''
    with open(yaml_file, 'r', encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def read_file(fname) -> str:
    '''Read text from file.'''
    with open(fname, 'r', encoding="utf-8") as f:
        return f.read()

def write_file(fname, content:str):
    '''Write content to file.'''
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

def copy_to(f: str, t: str):
    '''Copy file from one plcae to another.'''
    try:
        shutil.copyfile(f, t)
    except Exception:
        logging.error("Error while copy file: %s" % traceback.format_exc())
