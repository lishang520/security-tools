#coding=utf-8
'''
功能：
    对url进行批量的备案查询，获取到url所对应的公司
    对查询不到的结果，将其替换为 空，然后写入excel
实现原理：
        借助站长工具的批量查询接口：http://icp.chinaz.com/searchs
        通过子自动切换user-agent和延迟1秒来进行绕过限制
author：painter

'''
import requests,time
from lxml import etree
from random import choice
from openpyxl import Workbook



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



# 获取随机请求头
def get_headers():
    file = open('user_agent.txt', 'r',encoding='utf-8')
    user_agent_list = file.readlines()
    user_agent = str(choice(user_agent_list)).replace('\n', '')
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0' if len(
        user_agent) < 10 else user_agent
    headers = {
        'Host': "icp.chinaz.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "close",
        "User-Agent": user_agent,
        'Referer':'http://icp.chinaz.com/searchs',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length':'447',
        'Upgrade-Insecure-Requests':'1',
        'DNT':'1',
    }
    return headers


def split_target():
    #将目标进行分组，10个一组
    with open('result.txt','r',encoding='utf-8-sig') as f :
        data = f.readlines()

    b = [data[i:i + 10] for i in range(0, len(data), 10)]

    return b


def write_excel(datas):
    #u就是传入进来的原始url，t就是传入进来的公司名称
    # 实例化
    wb = Workbook()
    # 获取当前active的sheet
    sheet = wb.active
    # 打印表名
    # print(sheet.title)
    # 修改sheet名
    sheet.title = 'url备案查询结果'
    # 写数据
    # 添加标题
    sheet['A1'] = "url"
    sheet['B1'] = "备案信息"
    # 附加数据
    try :
        for i in datas:
            for m in i :
                u,t = m.split('+')
                sheet.append([u, t])

        wb.save("url备案信息.xlsx")
    except :
        pass


def query(msg):
    check_result = []
    headers = get_headers()

    url  = 'http://icp.chinaz.com/searchs'
    # print(info)
    info = '\n\r'.join([ m.strip() for m in msg])

    data = {
        'hosts':info,
        'btn_search':'%E6%9F%A5%E8%AF%A2',
        '__RequestVerificationToken=':'CfDJ8Fd2XTAM3cdBrz9uUkX_CfI-VnLKkILeETMahxB-HSmxdbOczHgjtNnPIo7hoLIO2KMFALyFHYsw01UpxvBZnFUe5kTV7e3tO6nPGi1FY0jAwSyNwqQI8YRfc1dvBKV3a2e9oJUsPwGACSaCjHxvz4s',
    }
    # proxy = {'https': 'https://http-dynamic.xiaoxiangdaili.com:10030','http':'http://http-dynamic.xiaoxiangdaili.com:10030'}

    html = requests.post(url=url,data=data,headers=headers).content.decode('utf-8')
    time.sleep(1)
    # print(html)
    req = etree.HTML(html)
    company_data = req.xpath('//*[@id="result_table"]/tr/td[2]/a')

    old_data = [ i.strip() for i in msg]
    print('url数量'+str(len(msg))+'----备案数量：'+str(len(company_data)))

    #进行判断，如果有的域名没查到，那么就让其为空
    for num in range(1,11):    #1到10
        if req.xpath('//*[@id="result_table"]/tr[{}]/td[2]/a'.format(num)) == []:     #进行判断，看是否有没查到的
            real_company = ''  #未查到，就设置为空
        else :
            real_company = req.xpath('//*[@id="result_table"]/tr[{}]/td[2]/a'.format(num))[0].text
        try :
            msg = old_data[num-1] + '+' + real_company     #用+号来连接，方便写入excel的时候进行拆分
            check_result.append(msg)     #将结果添加到列表里
        except:
            pass

    return check_result    #返回待写入的结果

if __name__ == '__main__':
    title()
    results = []     #用来储存最终的结果，并将其写入到excel
    data = split_target()

    for targets in data :
        result = query(targets)     #进行备案查询
        results.append(result)
    write_excel(results)    #写入excel
