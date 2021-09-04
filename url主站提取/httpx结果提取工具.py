# -*- coding: UTF-8 -*-
'''
将httpx的结果里的url提取出来
'''
def domain_extract()
    result = set()
    with open('edu_result.txt','r',encoding='utf-8') as f :
        message = f.readlines()
    for m in message :
        m = m.split('[')
        result.add(m[0].strip())

    #写入结果
    for info in result :
        with open('result.txt', 'a+', encoding='utf-8') as f:
            f.write(info+'\n')
