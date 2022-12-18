#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml, logging, traceback, shutil
import xml.sax
from typing import *

ANDROID_STRING_ELEMENT_TAG_NAME_STRING = "string"
ANDROID_STRING_ELEMENT_TAG_NAME_PLURALS = "plurals"
ANDROID_STRING_ELEMENT_TAG_NAME_STRING_ARRAY = "string-array"

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

def parse_xml(xmlfile: str) -> Dict[str, List[str]]:
    '''parse xml'''
    parser = xml.sax.make_parser()
    handler = AndroidStringHandler()
    parser.setContentHandler(handler)
    parser.parse(xmlfile)
    return handler.resources

class AndroidStringHandler(xml.sax.ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.resources = {}
        self.element_name = ''
        self.element_values = []
    
    def startElement(self, name, attrs):
        if name == ANDROID_STRING_ELEMENT_TAG_NAME_STRING\
            or name == ANDROID_STRING_ELEMENT_TAG_NAME_PLURALS\
            or name == ANDROID_STRING_ELEMENT_TAG_NAME_STRING_ARRAY:
            self.element_name = attrs["name"]
        return super().startElement(name, attrs)
    
    def endElement(self, name):
        if name == ANDROID_STRING_ELEMENT_TAG_NAME_STRING\
            or name == ANDROID_STRING_ELEMENT_TAG_NAME_PLURALS\
            or name == ANDROID_STRING_ELEMENT_TAG_NAME_STRING_ARRAY:
            element_values = []
            element_values.extend(self.element_values)
            self.resources[self.element_name] = element_values
            self.element_name = ''
            self.element_values = []
        return super().endElement(name)
    
    def characters(self, content: str):
        if len(self.element_name) > 0:
            content_stripped = content.strip()
            if len(content_stripped) > 0:
                self.element_values.append(content_stripped)
        return super().characters(content)

if __name__ == "__main__":
    value = parse_xml("/Users/wangshouheng/desktop/repo/github/leafnote/app/src/main/res/values/strings.xml")
    print(value)
