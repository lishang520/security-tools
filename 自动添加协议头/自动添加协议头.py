'''
功能：自动检测目标是不是带有http和https协议，如果不是，就通过给其添加http和https，
    然后request这两种可能，接着看状态码，状态码正常，则该协议存在
'''

import requests
import time


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



def check(target,data):
    protrol = ['http://', 'https://']
    result = ''   #必须要设置，否则一旦2次添加协议头都失败，则会报错
    if target.startswith('http://') or target.startswith('https://'):
        result = target
    else:
        for i in protrol:
            check = i + target   #拼接协议
            try :
                if requests.get(url=check,timeout = 4).status_code == 200:   #用拼接的协议的url进行请求
                    result = check
                    break
            except :            #必须要接收异常，因为当不是200，网页打不开的时候就会异常
                # print('{}不是{}协议'.format(url,i.replace('://','')))
                pass
    # print('协议添加成功>>>>>{}'.format(result))

    print(result)
    data.add(result)


def write_info(message):
    with open('result.txt','a+',encoding='utf-8') as f :
        for m in message :
            f.write(m+'\n')


def main():
    title()
    # file_name=input('请输入文件名>>>>')
    data = set()
    file_name='targets.txt'
    with open(file_name,'r',encoding='utf-8') as f :    #打开待检测的url
        urls = f.readlines()
    for url  in urls:
        url = url.strip()
        check(url,data)    #将结果添加到集合里
    write_info(data)


if __name__ == '__main__':
    main()

















