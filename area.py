from wxpy import *
from pyecharts import Map
import webbrowser

bot = Bot(cache_path=True)  # 弹出二维码登录微信，生成bot对象

allFriends = bot.friends()  # 获取所有的微信好友信息

areaDic = {}  # 定义一个空字典，用于存放省市以及省市人数

for friend in allFriends:
    if friend.province not in areaDic:
        areaDic[friend.province] = 1
    else:
        areaDic[friend.province] += 1

keys = area_dic.keys()
v = area_dic.values()

map = Map("好友地域分布", width=1200, height=600)
map.add("好友地域分布" ,keys, v, maptype='china', is_visualmap=True)
map.render("area.html")
webbrowser.open("area.html")