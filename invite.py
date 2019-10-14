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

# 注册机器人
bot = Bot(cache_path=True,console_qr = 2)
bot.enable_puid('wxpy_puid.pkl')
rebot = bot.groups().search('Goodog') # 需要加入的群

# 自动通过好友后发送的加群提示
allText = '回复关键词加群： \n\n1、羊毛（加入羊毛优惠群）\n2、py（加入机器人体验群）\n3、互粉（加入公众号互粉群）\n4、更多群敬请期待\n\n -PS: 如果回复关键字无效，请耐心等待手工拉入。'

# 自动通过好友请求
@bot.register(msg_types=FRIENDS)
def auto_audit_msg(msg):
    new_friend = bot.accept_friend(msg.card)
    new_friend.send('我是Goodog小助手，如果你也想拥有一个跟我一样功能的机器人请添加公众号【小夭同学】留言获取！')
    new_friend.send_raw_msg(
        raw_type=42,
        raw_content='<msg username="infopush" nickname="小夭同学"/>'
    ) 
    new_friend.send(allText)

# 关键字回复发送加群邀请链接
@bot.register(Friend, msg_types=TEXT)
def auto_add_msg(msg):
    if 'py' in msg.text.lower():
        rebot[0].add_members(msg.sender, use_invitation=True)
        msg.sender.send('如果加入py群失败，请等待人工邀请加入！！')

# 判断是否为新用户入群
invite_compile = re.compile(r'邀请"(.*?)"加入了群聊\s*$') 
# 新用户入群发送的公告
rebot_msg = '''@{atname}\u2005\u2005\u2005🌹🌹🌹欢迎加入群🌹🌹🌹\n
⚡⚡⚡⚡ 此群禁止发广告，不然踢！！！\n
💣💣💣 无法登录网页微信的问题，无有效解决办法。\n
🙋🙋🙋 怎样提问：\n
1. 不要问无意义的问题 🌡 
2. 问问题前最好贴出截图。🧸 
3. 描述清晰，信息充足。💎
4. 如果想要源码请关注💡 【小夭同学】💡 回复【帮助】获取'''

# 注册群来抓群群消息

@bot.register(rebot, NOTE)
def invite_group(msg):
    """ 群通知处理 """
    text = msg.text # 通知的内容
    member = msg.member.name # 消息发送者昵称
    invite_names = invite_compile.findall(text)  # 判断是否是加入了新用户
    if invite_names:  # 用于邀请
        invite_name = invite_names[0]  # 加入者的昵称
        if rebot_msg:
            note = rebot_msg.format(atname=invite_name)
            msg.sender.send(note)  # 向群里发送欢迎语句
        return
        
while True:
    schedule.run_pending()
    time.sleep(1)