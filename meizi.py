import os,re,tqdm,requests,sys,time,colorama
from urllib import request
from lxml import etree

def httpget(url):
    i=1
    while i<=3:
        try:
            headers={b'accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', b'accept-encoding': b'gzip, deflate, br', b'accept-language': b'zh-CN,zh;q=0.9', b'cache-control': b'max-age=0', b'cookie': b'UM_distinctid=17075d85cff10a-01607eb9ead8a8-376b4502-100200-17075d85d00120; CNZZDATA1255357127=319138885-1582524254-%7C1583800577', b'referer': b'https://www.meitulu.com/', b'sec-fetch-mode': b'navigate', b'sec-fetch-site': b'same-origin', b'sec-fetch-user': b'?1', b'upgrade-insecure-requests': b'1', b'user-agent': b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            r=requests.get(url=url,headers=headers,timeout=3)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            print(colorama.Back.RED+'发生错误：'+str(e))
            print('[{}/3]正在尝试重连！'.format(str(i)))
            i+=1
    print(colorama.Back.RED+'重连失败，请复制错误信息报告作者！')
    input('请按Enter键退出！')
    sys.exit()

def get_input(maxint,text):
    while True:
        userin=input(text)
        if userin.lower()=='q':sys.exit()
        if userin.isdecimal()==True:
            if int(userin)<=maxint and int(userin)>0:
                return int(userin)
                break
        print(colorama.Back.RED+'您的输入非法，请重新输入！')
        
class mtl():
    def __init__(self):
        self.host='https://www.meitulu.com'
        self.titles,self.allurls=[],[]

    def search(self):
        while True:
            while True:
                keyword=input('请输入搜索关键词： ')
                if keyword=='':print(colorama.Back.RED+'关键词不能为空！')
                elif keyword=='q':sys.exit()
                elif str.isalnum(keyword)==False:print(colorama.Back.RED+'您的输入非法，请重新输入！')
                else:break
                
            t0=time.time()
            url=self.host+'/search/'+keyword
            html=httpget(url)
            ehtml=etree.HTML(html)
            self.results=ehtml.xpath("//ul[@class='img']/li")
            if len(self.results)==0:
                print(colorama.Back.RED+'没有匹配的结果，换个关键词试试吧！')
            else:
                t1=time.time()
                print(colorama.Back.GREEN+'共找到匹配结果{}条，耗时{}秒'.format(str(len(self.results)),str(round(t1-t0,3))))
                break

    def makeurls(self):
        i=get_input(len(self.results),'请输入爬取图集数量： ')
        for result in self.results[:i]: #result：一个图集，self.results：所有图集
            title=result.xpath("./p[@class='p_title']/a/text()")[0] #获取图集标题
            str_num=result.xpath("./p[1]/text()")[0]
            num=re.search(r'(?<=：).*(?=张)', str_num).group().strip() #提取图片数量
            url0=result.xpath("./a/img/@src")[0].replace('0.jpg','{}.jpg') #图片链接模板

            urls=[] #用于储存一个图集中所有图片链接
            for i in range(int(num)): #生成图片链接
                urls.append(url0.format(str(i+1)))
   
            self.titles.append(title)
            self.allurls.append(urls)

    def download(self):
        i1=0 #下载图集数
        c=0 #下载图片计数
        t0=time.time()
        print('已开始下载任务！')
        for title in self.titles:
            print('-------------------->>正在下载第{}组，还剩{}组<<--------------------'.format(str(i1+1),str(len(self.titles)-i1-1)))
            print('    ·图册标题：'+title)
            fdir='./Photos/'+title+'/'
            if os.path.isdir(fdir) == False:
                os.makedirs(fdir)
            pbar=tqdm.tqdm(range(len(self.allurls[i1])),ascii=True,ncols=90)
            for i2 in pbar:
                path=fdir+'{}.jpg'.format(str(i2+1))
                if os.path.isfile(path)==False:
                    pbar.set_description_str(colorama.Fore.GREEN+'    ·下载进度')
                    try:
                        request.urlretrieve(self.allurls[i1][i2],path)
                        c+=1
                    except Exception:
                        pbar.set_description_str(colorama.Fore.RED+'    ·下载出错')
                        time.sleep(1.5)
                else:
                    pbar.set_description_str(colorama.Fore.YELLOW+'    ·图片已存在')
                    time.sleep(0.05)
            i1+=1
        t1=time.time()
        print(colorama.Back.GREEN+'\n已完成下载任务，共下载图集{}个（图片{}张），耗时{}秒'.format(str(i1),str(c),str(round(t1-t0,3))))

    def run(self):
        colorama.init(True)
        self.search()
        self.makeurls()
        self.download()
        
if __name__ == "__main__":
    os.system('title MeiTuLuSpider[V2] @吾爱破解 lihaisanhui')
    print('欢迎使用美图录Spider[V2,2020.03.11]！\n前往数据源：https://www.meitulu.com 下载更多精彩图片！\n')
    mtl=mtl()
    mtl.run()
    input('请按Enter键退出！')