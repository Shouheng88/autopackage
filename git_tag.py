#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, os
from apktool import *
from files import *
from logger import config_logging
from pathlib import Path

def add_new_tag(info: ApkInfo):
    '''Add current new tag.'''
    os.system("cd %s && git tag v%s && git push origin --tags" 
        % (config.gradlew_location, info.version_name))

def gen_git_log(info: ApkInfo):
    '''Generate git tag logs.'''
    # Get last commit log pattern. 
    last_git_tag = _find_last_git_tag()
    if len(last_git_tag) == 0:
        logi("Last git tag not found.")
        return
    _append_gitlog_to_markdown(info, last_git_tag)

def _append_gitlog_to_markdown(info: ApkInfo, last_git_tag: str):
    '''Append gitlog to markdown gitlog file.'''
    git_logs = os.popen(
        "cd %s && git log %s..HEAD --oneline" 
        % (config.gradlew_location, last_git_tag)
    ).read().strip()
    markdown_git_logs = ('## %s \n - ' % info.version_name)  + '\n- '.join(git_logs.split('\n'))
    content = ''
    if os.path.exists(config.output_gitlog_store_file):
        content = read_file(config.output_gitlog_store_file)
    content = markdown_git_logs + '\n' + content
    write_file(config.output_gitlog_store_file, content)
    _commit_git_log_change_event(info)
    return git_logs

def _commit_git_log_change_event(info: ApkInfo):
    '''Commit git log file to community repo.'''
    gitlog_store_file_path = Path(config.output_gitlog_store_file)
    gitlog_store_file_dir = gitlog_store_file_path.parent
    gitlog_store_file_name = os.path.basename(config.output_gitlog_store_file)
    os.system("cd %s\
        && git pull \
        && git add %s\
        && git commit -m \"feat: add upgrade logs for %s\"\
        && git push" 
        % (gitlog_store_file_dir, gitlog_store_file_name, info.version_name))

def _find_last_git_tag() -> str:
    '''Get last version git tag'''
    last_version_name = os.popen(
        "cd %s && git describe --abbrev=0 --tags" % (config.gradlew_location)).read().strip()
    return last_version_name

if __name__ == "__main__":
    config_logging()
    print(gen_git_log(ApkInfo(version_name="test")))
