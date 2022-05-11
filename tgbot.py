#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import telebot
import os, requests
from global_config import *
from logger import config_logging

# def send_message(tb: telebot.TeleBot, chat_id, msg):
#     tb.send_message(chat_id, msg)
#     print("Message Sent!")

TG_SEND_DOCUMENT_URL = 'https://api.telegram.org/bot%s/sendDocument'

def send_apk(path: str, name: str, msg: str):
    '''Send APK to TG channel by bot.'''
    if config.tg_chat_id is None or config.tg_chat_id == 0:
        logging.error("Failed to send APK to TG: chat id required!")
        return
    if config.tg_token is None or len(config.tg_token) == 0:
        logging.error("Failed to send APK to TG: chat token required!")
        return
    url = TG_SEND_DOCUMENT_URL % (config.tg_token)
    files = {
        'document': (name, open(path, 'rb'))
    }
    ret = requests.post(url, data={
        'chat_id': config.tg_chat_id,
        'caption': msg
    }, files=files)
    print(ret.text)

if __name__ == "__main__":
    '''Test entry.'''
    config_logging()
    config.parse()
    # tb = telebot.TeleBot("Bot")
    # tb.config['api_key'] = token
    # send_message(tb, chat_id, "This is funny. I'm using telegram bot to send message to you :D")
    send_apk('config.yml', "Hello!")
