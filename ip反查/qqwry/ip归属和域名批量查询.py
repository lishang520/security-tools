#!/usr/bin/python
#coding=utf-8
'''
功能：ip查所属城市、公司、反查域名，并写入excel
author:painter

'''

from qqwry import QQwry
import re,time,sys
from openpyxl import Workbook
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import  ThreadPoolExecutor,ProcessPoolExecutor  #导入线程池模块
import json
import requests
from lxml import etree
import hashlib
import traceback

#该模块用作个人logo，直接调用即可
def title():
    print('''                                                                                                                                                                                                                                                   
                                            iiii                             tttt                                                  
                                           i::::i                         ttt:::t                                                  
                                            iiii                          t:::::t                                                  
                                                                          t:::::t                                                  
    ppppp   ppppppppp     aaaaaaaaaaaaa   iiiiiii nnnn  nnnnnnnn    ttttttt:::::ttttttt        eeeeeeeeeeee    rrrrr   rrrrrrrrr   
    p:::::::::::::::::p   aaaaaaaaa:::::a  i::::i n::::::::::::::nn t:::::::::::::::::t     e::::::eeeee:::::eer:::::::::::::::::r 
    pp::::::ppppp::::::p           a::::a  i::::i nn:::::::::::::::ntttttt:::::::tttttt    e::::::e     e:::::err::::::rrrrr::::::r
     p:::::p     p:::::p    aaaaaaa:::::a  i::::i   n:::::nnnn:::::n      t:::::t          e:::::::eeeee::::::e r:::::r     r:::::r
     p:::::p     p:::::p  aa::::::::::::a  i::::i   n::::n    n::::n      t:::::t          e:::::::::::::::::e  r:::::r     rrrrrrr
     p:::::p     p:::::p a::::aaaa::::::a  i::::i   n::::n    n::::n      t:::::t          e::::::eeeeeeeeeee   r:::::r            
     p:::::p    p::::::pa::::a    a:::::a  i::::i   n::::n    n::::n      t:::::t    tttttte:::::::e            r:::::r            
     p:::::ppppp:::::::pa::::a    a:::::a i::::::i  n::::n    n::::n      t::::::tttt:::::te::::::::e           r:::::r            
     p::::::::::::::::p a:::::aaaa::::::a i::::::i  n::::n    n::::n      tt::::::::::::::t e::::::::eeeeeeee   r:::::r                  
     p::::::pppppppp      aaaaaaaaaa  aaaaiiiiiiii  nnnnnn    nnnnnn          ttttttttttt      eeeeeeeeeeeeee   rrrrrrr            
     p:::::p                                                                                                                                                                                                                                            
    p:::::::p                                                                                                                      
    p:::::::p                                                                                                                
    p:::::::p                                    What is black and what is white                                                                              
    ppppppppp                                    blog： https://lishang520.github.io/                                                                                                                                                                                                                                                    
    ''')

title()

def proxy():
    #熊猫代理注册链接：http://www.xiongmaodaili.com?invitationCode=C34F143A-7D85-4A22-BE1D-A19E5972E816
    #通过请求api获取ip，请求一次获取一个，直到用完，仅仅针对高效代理
    #以下是通过api，是高效代理
    url= "http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=63b3d3d2bc96fd015ec7a51f128b5594&orderNo=GL20190826200547EFi2A2C0&count=1&isTxt=0&proxyType=1"
    req = requests.get(url=url).content.decode('utf-8')
    req = json.loads(req)    #将str转换为json格式
    data = req.get('obj')   #获取ip和端口，一个一个的取，请求一次取一个
    # proxy_ip = 'http://{}:{}'.format(data[0].get('ip'),data[0].get('port'))     #组合ip
    proxy_ip = {'https':'https://{}:{}'.format(data[0].get('ip'),data[0].get('port'))}
    print(proxy_ip)
    return proxy_ip

def Dynamic_proxy(checkUrl):
    #动态代理专用
    _version = sys.version_info
    is_python3 = (_version[0] == 3)

    # 个人中心获取orderno与secret
    orderno = "DT20210213192509HJKQ1f72"
    secret = "4d0bcfe08432afbffb00e602d52baf68"
    ip = "dynamic.xiongmaodaili.com"
    #按量订单端口
    port = "8088"
    #按并发订单端口
    #port = "8089"

    ip_port = ip + ":" + port

    timestamp = str(int(time.time()))  # 计算时间戳
    txt = ""
    txt = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        txt = txt.encode()

    md5_string = hashlib.md5(txt).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写

    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp + "&change=true"

    # http协议的网站用此配置
    proxy = {"https": "https://" + ip_port}
    # https协议的网站用此配置
    # proxy = {"https": "https://" + ip_port}
    print('\033[0;31m页面无法正常访问，设置代理中：{}！\033[0;31m'.format(proxy))
    headers = {"Proxy-Authorization": auth,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

    # http协议可用性检测，每访问一次返回的结果换一个IP即为代理成功
    url = checkUrl
    print(url)
    r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)   #此处若报错，则回到上个域里的错误接收页面，继续循环执行该函数，知道代理并且访问成功
    return r #返回页面数据




def query_ip(target,ip):
    #查询ip归属
    q = QQwry()
    q.load_file('qqwry.dat')
    info = q.lookup(target)
    daomain = searchIP(target)
    result = {str(ip):{   str(info):daomain    }   }    #ip + 归属 + 反查的域名
    print(result)
    result_finall.update(result)

def searchIP(ip: str):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'close',
        'Referer': 'http://www.baidu.com/'
    }

    checkUrl = "https://site.ip138.com/" + ip


    while True:
        try :
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            resp = requests.get(url=checkUrl,headers=headers)     #必须要用  **var来自解压之前设置的字典格式的参数
            #若print语句正常执行，则代表ip没被禁用，页面可以正常访问
            print('\033[1;32m 未使用代理，页面正常！\033[1;32m')    #绿色字体显示：\033[1;32m
            break

        except :
            #ip被禁，报错
            # traceback.print_exc()   #调试错误专用
            resp = Dynamic_proxy(checkUrl)   #如果该函数调用中代理访问页面出错，则一直执行该函数，直到代理并且访问成功
            #如果没报错，就代表代理成功并且访问页面成功，则跳出循环
            break

    selector = etree.HTML(resp.text)
    content = selector.xpath('//span[@class]/../a/text()')
    if content == []:  # 判断列表是否为空,如果为空，就将None添加到该空列表
        content.append('None')
    print(content)
    return content



def write_info(data):
    #写入excel
    # 实例化
    wb = Workbook()
    # 获取当前active的sheet
    sheet = wb.active
    # 打印表名
    # print(sheet.title)
    # 修改sheet名
    sheet.title = 'ip归属和域名信息'
    # 写数据
    # 添加标题
    sheet['A1'] = "ip"
    sheet['B1'] = "归属城市"
    sheet['C1'] = "归属公司"
    sheet['D1'] = "域名"
    # 附加数据
    # print(data)
    for p in data.items() :
        info_belong = p[1].items()   #归属信息+域名
        info_belong = list(info_belong)[0]
        info_addr= info_belong[0]#归属信息
        info_doamin = info_belong[1]  #反查的域名
        # print(info_doamin)
        if info_doamin == None :
            info_doamin = 'None'
        city = eval(info_addr)[0]   #讲一个类似于列表结构的字符串转换为列表
        company = eval(info_addr)[1]  # 讲一个类似于列表结构的字符串转换为列表
        print('{}--{}--{}--{}'.format(p[0],city,company,info_doamin))   #p[0]是ip

        sheet.append([p[0], city,company,str(info_doamin)])    #写入每一条数据,将归属信息转换为元组模式,必须要将info_domain转换为str格式，否则如果有多个域名就会报错
    #保存数据
    wb.save("ip归属信息(查询完毕).xlsx")



if __name__ == '__main__':
    title()
    result_finall = {}
    with open('targets.txt','r',encoding='utf-8') as f :
        message = f.readlines()
        # 创建线程池
        with ThreadPoolExecutor(10) as t:

            for m in message:
                m = m.strip()
                ip = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",m)  #匹配ip
                for i in ip :
                    t.submit(query_ip, i,m)  # 提交任务

    write_info(result_finall)
