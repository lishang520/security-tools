import json
from openpyxl import Workbook
import re,sys

class Extract_information():
    def __init__(self,filename):
        self.target_file = filename    #获取目标文件名
        self.web_assets=[]   #存放web资产，将http和https协议的放在该列表
        self.other_assets=[]   #存放 非 web资产
        self.keyword = ['ApplicationComponent', 'Protocol','URL','AppDigest', 'IPAddr','Port', 'ProductName', 'Version','Info','OperatingSystem','DeviceType','StatusCode']
        self.sheet1_name = 'web资产'
        self.sheet2_name = '非web资产'
        self.result_file = 'kscan提取结果.xlsx'
        self.ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')       #数据清洗，清楚特殊字符，防止无法写入excel，搭配58行使用
        self.title()
        self.banner()

    def title(self):
        print('\033[1;31m+------------------------------------------')
        print('+  安全团队:  base64-sec                           ')
        print('+      作者:  base64_painter                   ')
        print('+------------------------------------------\033[0m')

    def banner(self):
        print('''
        用法：请提供kscan导出来的json文件
            python3 kscan结果提取.py  xx.json
        ''')

    def check_assets(self):
        with open(self.target_file, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        for msg in ret_dic:
            protocol = msg['Protocol']
            if protocol == 'https' or protocol == 'http':
                self.web_assets.append(msg)
            else:
                self.other_assets.append(msg)


    def write_into_excel(self):
        print("[+]开始提取信息，正在写入excel中，请等待...")
        # 实例化
        wb = Workbook()
        # 获取当前active的sheet
        sheet1 = wb.active
        sheet1.title = self.sheet1_name
        sheet2 = wb.create_sheet(self.sheet2_name,1)  #创建表2
        # 打印表名
        # 修改sheet名
        num = 0   #开关，用来控制下面的遍历
        for sheet in [sheet1,sheet2]:
            if num  == 0:
                data = self.web_assets
                num = num +1
            else :
                data = self.other_assets
            chars = []
            # print(type(sheet['A1']))
            for i in range(65,65+len(self.keyword)):
                chars.append(chr(i))
            for index in range(len(chars)):
                sheet['{}1'.format(chars[index])]  = self.keyword[index]

            #下面开始写入数据-----------------
            for info in data:

                temp_info = []
                for k in self.keyword:
                    one_pice_info = self.ILLEGAL_CHARACTERS_RE.sub(r'',str(info.get(k)))
                    # print(one_pice_info)
                    temp_info.append(one_pice_info)
                # print(temp_info)
                sheet.append(temp_info)


        wb.save(self.result_file)   #保存表格
        print("[+]提取成功，请前往 {} 中查看".format(self.result_file))



if __name__ == '__main__':
    file_name = sys.argv[1]
    example = Extract_information(file_name)   #传入目标文件名
    example.check_assets()
    example.write_into_excel()

