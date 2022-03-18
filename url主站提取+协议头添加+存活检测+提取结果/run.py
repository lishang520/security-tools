import tldextract,os,subprocess

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
    ppppppppp                                    blog： https://www.cnblogs.com/painter-sec  
                                                 Team： base64 安全团队                                                                                                                                                                                                                                              
    ''')


def get_domain(urls):
    url = 'http://m.windowscentral.com'
    temp = set()
    for url in urls :
        # 一级域名
        domain = tldextract.extract(url).domain
        # 二级域名
        subdomain = tldextract.extract(url).subdomain
        # 后缀
        suffix = tldextract.extract(url).suffix
        # print("获取到的一级域名:{}".format(domain))
        # print("获取到二级域名:{}".format(subdomain))
        # print("获取到的url后缀:{}".format(suffix))
        if subdomain == 'com' or subdomain == 'cn' or subdomain == 'net'  :
            temp.add(subdomain+'.'+domain+'.'+suffix)
        else :
            temp.add(domain+'.'+suffix)
    return temp
def load_file():
    with open('urls.txt','r',encoding='utf-8') as f:
        message = f.readlines()
    return message

def write_file(results,name):
    with open(name,'a+',encoding='utf-8') as f :
        for i in results:
            f.write(i+'\n')


def domain_extract():
    result = set()
    with open('wait_extract.txt','r',encoding='utf-8') as f :
        message = f.readlines()
    for m in message :
        m = m.split('[')
        result.add(m[0].strip())

    #写入结果
    for info in result :
        with open('result.txt', 'a+', encoding='utf-8') as f:
            f.write(info+'\n')

def domain_verify():
    os.system('httpx -l wait_verify.txt  -ip >> wait_extract.txt')


if __name__ == '__main__':
    title()
    data = load_file()
    targets = get_domain(data)
    write_file(targets,'wait_verify.txt')
    # print('''
    # 注意：下面的步骤需要手工操作
    #     在当前目录地址栏输入cmd，然后输入命令：httpx -l wait_verify.txt  -ip >> wait_extract.txt
    #     等待命令执行完毕，执行完毕后按下在该窗口按下回车，继续向下执行
    # ''')
    # input('如果httpx执行完毕，请输入回车：>>>>>>>')
    domain_verify()
    domain_extract()