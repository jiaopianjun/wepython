#coding=utf8
import requests
from requests import exceptions
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from threading import Timer
import re
from wxpy import *
import  schedule
import  time
import http
import  json 
import datetime
import random
import os
import ctypes

bot = Bot(cache_path=True,console_qr = 2)
myself = bot.self
bot.enable_puid('wxpy_puid.pkl')


sync = ensure_one(bot.groups().search('同步'))
lie = ensure_one(sync.search('Lie'))
Goodog = ensure_one(sync.search('Goodog'))

# 群消息同步
@bot.register(sync)
def sync(msg):
    if msg.member == Goodog:
        msg.forward(lie, prefix='群消息同步：'+'\n')


while True:
    schedule.run_pending()
    time.sleep(1)
