from wxpy import *
from PIL import Image
import os
import math
# 创建头像存放文件夹
def create_file_path():
    avater_dir = os.path.join(os.getcwd(),'wechat')
    if not os.path.exists(avater_dir):
        os.mkdir(avater_dir)
    return avater_dir

# 获取所有的好友头像并保存
def save_wx_avater(avater_dir):
    bot = Bot(cache_path=True)
    friends = bot.friends(update=True)
    num = 0
    nameList = []
    for friend in friends:
        friend.get_avatar(os.path.join(avater_dir,f'{str(num)}.jpg'))
        nameList.append(friend.name)
        print("好友昵称：%s"%friend.name)
        num += 1

    with open('微信好友昵称.txt', 'w+', encoding='utf-8')as f:
        for n in nameList:
            f.write('"'+n+"',\n")
        f.close()
        print("程序结束：")
    print(nameList)

if __name__ == '__main__':
    avatar_dir = create_file_path()
    save_wx_avater(avatar_dir)