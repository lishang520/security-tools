'''def is_edu_id(ip: str) -> bool:
作者：painter

功能：判断一个目标是不是教育网的ip
实现方法：
        1、先判断待检测目标里是否包含'edu.cn'关键字，若包含，则直接写入文件
        2、本地读取目标（我带检测的目标），就将目标将其转换为ip
            如果目标里包含ip地址，比如:http://192.168.16.56  就通过re将其提取出来，并return回去
            如果目标里不包含ip，它可能就是类似于baidu.com,所以我需要将其解析为ip
        3、从教育网ip池爬取ip
        4、根据2获得的ip，和我们1爬取的ip进行比对，如果2获取的ip在1获取的ip里，那么它就是教育网ip

待检测ip：
https://124.165.196.3:4430
baidu.com
http://117.187.230.194:10000
58.205.208.9


核心：步骤4使用的ip来进行判断，该ip必须要是字符串类型，而我们通过正则匹配的ip是一个列表，所以我们在return返回数据的时候，只需要返回第一个元素即可

难点：
    1、异常信息为：Unsupported data type: <class 'list'>
    2、执行完本程序，只显示了一个结果，就一个   not   ,按道理应该是4个结果，而且这个not应该是第一个目标的，为啥其和第二个目标baidu.com 匹配上了



'''

import http.client
import re
import IPy
import socket
import threadpool

def target_to_ip(tg):
    '''
    将目标转换为ip，方便判断是否是edu的ip
    :return:
    '''

    # def isIP(str):
    #     '''
    #     判断是否是ip
    #     '''
    #     p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    #     if p.match(str):
    #         return True
    #     else:
    #         return False

    def getIP(domain):
        '''
        将域名解析为ip
        '''
        myaddr = socket.getaddrinfo(domain, None)
        return myaddr[0][4][0]  # 返回ip

    try:
        #提取目标里的ip
        result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", tg)     #提取ip

        #如果提取的result为none，则代表其实类似于baidu.com的url
        if result:
            #提取成功，直接返回该ip
            return result[0]
        else:
            #提取的result结果为None，所以需要对该url进行解析ip
            temp = tg.replace('http://', '').strip()  # 去掉http://
            temp = temp.replace('https://', '').strip()  # 去掉https://
            #去掉域名最后面的斜杠
            temp=temp.replace('.com/','.com')
            temp = temp.replace('.cn/', '.cn')
            temp = temp.replace('.org/', '.org')
            temp = temp.replace('.net/', '.net')
            result = getIP(temp)  # 获取解析来的ip

            return result    #返回解析的ip

    except:
        pass


def get_html(host, path):
    conn = http.client.HTTPConnection('ipcn.chacuo.net')
    conn.request("GET", '/view/i_CERNET')
    res = conn.getresponse()
    return res.read().decode("utf-8")


def is_edu_ip(target: str) -> bool:
    #1、先判断待检测目标里是否包含'edu.cn'关键字，若包含，则直接写入文件
    if 'edu.cn' in target:
        print(target+ '  ---------------------------- 是教育网')
        with open(r'edu_result.txt', 'a+', encoding='utf-8') as f:
            f.write(target+'\n')    #将结果写入
        return True

    #2、将目标转换为ip
    ip = target_to_ip(target)    #此时获取到的就是经过转换和提取的ip

    # 3. 获取教育网IP列表
    html = get_html('ipcn.chacuo.net', '/view/i_CERNET')
    res = re.findall(r'<span class="v_l">(.*)</span><span class="v_r">(.*)</span>', html)

    # 4. 判断当前ip是否在教育网IP中

    for iplist in res :
        #遍历教育网的列表

        if ip in IPy.IP('{}-{}'.format(iplist[0], iplist[1])) :
            #如果我们经过转换来的ip在教育网的列表里，那么我们的ip就是教育网ip
            result = target + '  ---------------------------- 是教育网'
            with open(r'edu_result.txt', 'a+', encoding='utf-8') as f:
                f.write(target +'\n')    #将结果写入
            print(result)     #打印属于教育网的目标
            return True       #结束此次ip的匹配
        else :
            continue    #若该目标在第一次匹配没匹配上，那么继续匹配，知道匹配完所有的可能
    print(target + '----not')    #目标在上面所有的可能全部匹配完了之后，还没匹配到，那么它就不属于教育网ip
    return False    #该目标不属于教育网，那么就结束该目标的匹配


if __name__ == '__main__':
    print('edu目标检测---------painter')
    #多线程
    urls = [l.strip() for l in open('./ip.txt', 'r')]
    pool = threadpool.ThreadPool(30)
    reqs = threadpool.makeRequests(is_edu_ip, urls)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


    #非多线程，不建议使用
    # with open(r'ip.txt', 'r', encoding='utf-8') as f:
    #     ip = f.readlines()    #读取所有的待测目标
    #
    # for url in ip :      #遍历所有的待测目标
    #     try :
    #         url=url.strip()    #去掉\n
    #         is_edu_ip(url)     #执行ip判断函数
    #     except Exception as e:
    #         pass

