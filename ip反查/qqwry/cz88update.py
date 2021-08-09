# coding=utf-8
#
# 用于从纯真网络(cz88.net)更新qqwry.dat
# for Python 3.0+
# 来自 https://pypi.python.org/pypi/qqwry-py3
#
# 用法：
# from cz88update import updateQQwry
# result = updateQQwry(filename)
#
# ﻿当参数filename是str类型时，表示要保存的文件名。
# 成功后返回一个正整数，是文件的字节数；失败则返回一个负整数。
#
# ﻿当参数filename是None时，函数直接返回qqwry.dat的文件内容（一个bytes对象）。
# 成功后返回一个bytes对象；失败则返回一个负整数。这里要判断一下返回值的类型是bytes还是int。
#
# 负整数表示的错误：
# ﻿-1：下载copywrite.rar时出错
# ﻿-2：解析copywrite.rar时出错
# ﻿-3：下载qqwry.rar时出错
# ﻿-4：qqwry.rar文件大小不符合copywrite.rar的数据
# ﻿-5：解压缩qqwry.rar时出错
# ﻿-6：保存到最终文件时出错

import struct
import urllib.request
import zlib
import logging
from typing import Union

__all__ = ('updateQQwry',)

logger = logging.getLogger(__name__)

def updateQQwry(filename: Union[str, None]) -> Union[int, bytes]:
    '''1.当参数filename是str类型时，表示要保存的文件名。
       成功后返回一个正整数，是文件的字节数；失败则返回一个负整数。

       2.当参数filename是None时，函数直接返回qqwry.dat的文件内容（一个bytes对象）。
       成功后返回一个bytes对象；失败则返回一个负整数。
       这里要判断一下返回值的类型是bytes还是int。'''
    def get_fetcher():
        # no proxy
        proxy = urllib.request.ProxyHandler({})
        # opener
        opener = urllib.request.build_opener(proxy)

        def open_url(file_name, url):
            # request对象
            headers = {
            'User-Agent': 'Mozilla/3.0 (compatible; Indy Library)',
            'Host': 'update.cz88.net'
            }
            req = urllib.request.Request(url, headers=headers)

            try:
                # r是HTTPResponse对象
                r = opener.open(req, timeout=60)
                dat = r.read()
                if not dat:
                    raise Exception('文件大小为零')
                return dat
            except Exception as e:
                logger.error('下载%s时出错: %s' % (file_name, str(e)))
                return None

        return open_url

    fetcher = get_fetcher()

    # download copywrite.rar
    url = 'http://update.cz88.net/ip/copywrite.rar'
    data = fetcher('copywrite.rar', url)
    if not data:
        return -1

    # extract infomation from copywrite.rar
    if len(data) <= 24 or data[:4] != b'CZIP':
        logger.error('解析copywrite.rar时出错')
        return -2

    version, unknown1, size, unknown2, key = \
        struct.unpack_from('<IIIII', data, 4)
    if unknown1 != 1:
        logger.error('解析copywrite.rar时出错')
        return -2

    # download qqwry.rar
    url = 'http://update.cz88.net/ip/qqwry.rar'
    data = fetcher('qqwry.rar', url)
    if not data:
        return -3

    if size != len(data):
        logger.error('qqwry.rar文件大小不符合copywrite.rar的数据')
        return -4

    # decrypt
    head = bytearray(0x200)
    for i in range(0x200):
        key = (key * 0x805 + 1) & 0xff
        head[i] = data[i] ^ key
    data = head + data[0x200:]

    # decompress
    try:
        data = zlib.decompress(data)
    except:
        logger.error('解压缩qqwry.rar时出错')
        return -5

    if filename == None:
        return data
    elif type(filename) == str:
        # save to file
        try:
            with open(filename, 'wb') as f:
                f.write(data)
            return len(data)
        except:
            logger.error('保存到最终文件时出错')
            return -6
    else:
        logger.error('保存到最终文件时出错')
        return -6

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ret = updateQQwry(sys.argv[1])
        if ret > 0:
            print('成功更新到%s，%s字节' %
                  (sys.argv[1], format(ret, ','))
                  )
        else:
            print('更新失败，错误代码：%d' % ret)
    else:
        print('用法：以想要保存的文件名作参数。')
