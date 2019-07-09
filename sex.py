from wxpy import *
import webbrowser
from pyecharts import Pie


bot = Bot(cache_path=True)  # 弹出二维码登录微信，生成bot对象

allFriends = bot.friends()  # 获取所有的微信好友信息

type = ['男同学','女同学','外星人']  # 男/女/未知性别好友名称

v = [0, 0, 0]  # 初始化对象好友数量

# 遍历所有好友，判断该好友性别
for friend in friends:
    if friend.sex == 1:
        v[0] += 1
    elif friend.sex == 2:
        v[1] += 1
    else:
        v[2] += 1

pie = Pie("好友性别分布")

pie.add("", type, v, is_label_show=True)

pie.render("sex.html")

webbrowser.open('sex.html')