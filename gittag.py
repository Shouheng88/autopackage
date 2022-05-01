#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, os
from apktool import *
from files import *
from assemble import YAML_CONFIGURATION_FILE_PATH
from logger import config_logging
from typing import List

# The directory to store the git logs. 
COMMUNITY_LOGS_DIR = "D:/codes/other/LeafNote-Community/logs"

def gen_git_tag(info: ApkInfo):
    '''Generate git tag logs.'''
    # Get last commit log pattern. 
    last_tag = _get_last_git_tag(info)
    if len(last_tag) == 0:
        return
    os.system("cd .. && git show v%s >> autopackage/temp" % (last_tag))
    details = read_file("temp")
    if len(details) == 0:
        logging.error("Failed to read git log commit info, since it's empty!")
        return
    pattern = details.splitlines()[0]
    logging.debug("The git commit log is: %s" % pattern)
    os.remove("temp")
    # Read commit logs from current to last commit log. 
    if pattern.startswith("commit"):
        os.system("cd .. && git log >> autopackage/temp")
        details = read_file("temp")
        os.remove("temp")
        lines = details.splitlines()
        logs = []
        for line in lines:
            line = line.strip()
            if len(line) > 0 \
                and not line.startswith("commit")\
                    and not line.startswith("Author:")\
                    and not line.startswith("Date:"):
                        logs.append(line)
            # End the loop. 
            if line.startswith(pattern):
                break
        _write_git_logs(info, logs)
        _commit_git_logs(info)
    else:
        logging.error("Failed to read git log commit info, since not found!")

def _write_git_logs(info: ApkInfo, logs: List[str]) -> str:
    '''Write git logs to file and commit to community.'''
    content = "\n".join(logs)
    if not os.path.exists(COMMUNITY_LOGS_DIR):
        os.mkdir(COMMUNITY_LOGS_DIR)
    path = os.path.join(COMMUNITY_LOGS_DIR, info.vname + ".txt")
    write_file(path, content)

def _commit_git_logs(info: ApkInfo):
    '''Commit git log file to community repo.'''
    os.system("cd %s\
        && git pull \
        && git add .\
        && git commit -m \"feat: add upgrade logs for %s\"\
        && git push" 
        % (COMMUNITY_LOGS_DIR, info.vname))

def _get_last_git_tag(info: ApkInfo) -> str:
    '''Get last git tag'''
    configurations = read_yaml(YAML_CONFIGURATION_FILE_PATH)
    apk_copy_to = configurations['dest']['apk_dir']
    last_version = 0
    last_version_name = ''
    for dir in os.listdir(apk_copy_to):
        parts = dir.split('_')
        if len(parts) > 1:
            vcode = parts[1]
            if not info.vcode == vcode and int(vcode) > last_version:
                last_version = int(vcode)
                last_version_name = parts[0]
    return last_version_name

if __name__ == "__main__":
    config_logging()
    print(_get_last_git_tag(ApkInfo()))
    print(gen_git_tag(ApkInfo(vname="test")))
