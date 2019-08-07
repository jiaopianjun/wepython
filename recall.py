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

bot = Bot(cache_path=True,console_qr = 1)
myself = bot.self
bot.enable_puid('wxpy_puid.pkl')



Lie = bot.friends().search(u'Lie')


Test = bot.groups().search(u'Test') 
recallNotice = ensure_one(bot.groups().search('recallNotice'))  // 改成你要转发的群 或者 个人微信号

# 文本 TEXT = 'Text'
# 位置 MAP = 'Map' 1
# 名片 CARD = 'Card' 2
# 分享 SHARING = 'Sharing' 3
# 图片 PICTURE = 'Picture'  4
# 语音 RECORDING = 'Recording' 5
# 文件 ATTACHMENT = 'Attachment' 6
# 视频 VIDEO = 'Video' 7


@bot.register(Group)

def handleReceiveMsg(msg):
    '''
    监听消息
    :param msg:
    :param chats:
    :return:
    '''
    ra = msg.raw
    mss = msg.bot.messages
    le = len(mss)
 
    if ra['Status'] == 4:
        # 获取消息ID
        oldmsgid = re.search(re.compile('<msgid>(.*?)</msgid>', re.S),ra['Content']).group(1)
        for i in range(le-1,-1,-1):
            if oldmsgid == str(mss[i].id):
                name = msg.chat.name
                username = msg.member.nick_name
                if name == None or name == '':
                    name = msg.chat.nick_name
                    username = msg.member.nick_name
                if mss[i].type == 'Text':
                    recallNotice.send('来自【'+ name + '】的【' + username +'】撤回了一条消息：'+ mss[i].text)
                    bot.file_helper.send('来自【'+ name + '】的【' + username +'】撤回了一条消息：'+ mss[i].text)
                    break
                elif mss[i].type == 'Map':
                    recallNotice.send('来自【'+ name + '】的【' + username + '】撤回了一个位置信息：' + (mss[i].location)['label'])
                    bot.file_helper.send('来自【'+ name + '】的【' + username + '】撤回了一个位置信息：' + (mss[i].location)['label'])
                    break
                elif mss[i].type == 'Card':
                    card = mss[i].card
                    name = card.name
                    if name == None or name == '':
                        name = card.nick_name
                    sex = str(card.sex)
                    if sex == '1':
                        sex = '男'
                    else:
                        sex = '女'
                    recallNotice.send('来自【'+ name + '】的【' + username + '】撤回了一张名片：名称：'+ name +',性别：' + sex)
                    bot.file_helper.send('来自【'+ name + '】的【' + username + '】撤回了一张名片：名称：'+ name +',性别：' + sex)
                    break
                elif mss[i].type == 'Sharing':
                    recallNotice.send('来自【'+ name + '】的【' + username + '】撤回了一个分享：' + mss[i].url)
                    bot.file_helper.send('来自【'+ name + '】的【' + username + '】撤回了一个分享：' + mss[i].url)
                    break
                elif mss[i].type == 'Picture':
                    mss[i].raw.get('Text')(mss[i].file_name)
                    bot.file_helper.send('来自【'+ name + '】的【' + username + '】撤回了一张图片，图片正在加载。。。')
                    bot.file_helper.send_image(mss[i].file_name)


                    recallNotice.send('来自【'+ name + '】的【' + username + '】撤回了一张图片，图片正在加载。。。')
                    recallNotice.send_image(mss[i].file_name)

                    break
                elif mss[i].type == 'Recording':
                    mss[i].raw.get('Text')(mss[i].file_name)
                    bot.file_helper.send('来自【'+ name + '】的【' + username + '】撤回了一条语音，语音正在加载。。。')
                    bot.file_helper.send_file(mss[i].file_name)

                    recallNotice.send('来自【'+ name + '】的【' + username + '】撤回了一条语音，语音正在加载。。。')
                    recallNotice.send_file(mss[i].file_name)
                    break
                elif mss[i].type == 'Attachment':
                    mss[i].raw.get('Text')(mss[i].file_name)
                    bot.file_helper.send('来自【'+ name + '】的【' + username + '】撤回了一个文件，文件正在加载。。。')
                    bot.file_helper.send_file(mss[i].file_name)

                    recallNotice.send('来自【'+ name + '】的【' + username + '】撤回了一个文件，文件正在加载。。。')
                    recallNotice.send_file(mss[i].file_name)
                    break
                elif mss[i].type == 'Video':
                    mss[i].raw.get('Text')(mss[i].file_name)
                    bot.file_helper.send('来自【'+ name + '】的【' + username +'】撤回了一个视频，视频正在加载。。。')
                    bot.file_helper.send_video(mss[i].file_name)

                    recallNotice.send('来自【'+ name + '】的【' + username +'】撤回了一个视频，视频正在加载。。。')
                    recallNotice.send_video(mss[i].file_name)
                    break

while True:
    schedule.run_pending()
    time.sleep(1)
    