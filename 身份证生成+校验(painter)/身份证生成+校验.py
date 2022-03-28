import random
import re
from datetime import datetime, timedelta
# 导入区域信息
import area
def title():
    print('\033[1;31m+------------------------------------------')
    print('+  安全团队:  base64-sec                           ')
    print('+      作者:  base64_painter                   ')
    print('+------------------------------------------\033[0m')
class IdCardNumber(str):
    """
    用于对身份证号码进行处理
    20210801 test OK
    """

    def __init__(self, id_card_number:str):
        super(IdCardNumber, self).__init__()
        self.id = id_card_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_area_name(self):
        """根据区域编号取出区域名称"""
        return area.AREA_INFO[self.area_id]

    def get_birthday(self):
        """通过身份证号获取出生日期(只支持18位身份证，返回YYYY-MM-DD格式的日期字符串)"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_birth(self) -> str:
        """
        通过身份证号码获取出生日期(返回8位日期字符串，支持15或18位身份证）
        :return birth:出生日期
        :rtype birth: str
        """
        number_length = len(self.id)
        if number_length == 18:
            birth = self.id[6:14]
            return birth
        elif number_length == 15:
            birth = '19' + self.id[6:12]  #目前的15位身份证是19xx年出生
            return birth
        else:
            return "ERROR"

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_sex(self):
        """通过身份证号获取性别， 女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @staticmethod
    def get_checkcode(digital_ontology_code:str) -> str or bool:
        """
        静态方法，从身份证号码前17位数字本体码计算第18位校验码
        :param digital_ontology_code:   17位数字本体码
        :type digital_ontology_code: str
        :return str(vi[remainder]): 18位身份证的最后1位校验码
        :rtype str(vi[remainder]): str
        """
        ai = []  # 17位数字本体码按位分割的列表,先创建列表，后面再赋值
        wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 加权因子列表
        vi = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]   # 校验码列表
        remainder = None # 用于在校验码列表中找校验码的模 （先赋值为None，后面再计算赋值）
        if len(digital_ontology_code) == 17:
            s = 0
            for i in digital_ontology_code:
                ai.append(int(i))
            for i in range(17):
                s = s + wi[i] * ai[i]  # 计算和
            remainder = s % 11  # 计算模
            return  str(vi[remainder])  # 通过模的值在校验码列表中找到对应的校验码并返回str
        else:
            return False

    def fifteen_to_eighteen(self) -> str:
        """
        15位身份证转18位身份证

        15变18，就是出生年份由2位变为4位，最后加了一位用于验证。验证位的规则如下：
        1、将前面的身份证号码17位数分别乘以不同的系数。从第一位到第十七位的系数分别为:7. 9 .10 .5. 8. 4. 2. 1. 6. 3. 7. 9. 10. 5. 8. 4. 2.
        2、将这17位数字分别和系数相乘的结果相加。
        3、用加出来和除以11，看余数是多少?
        4 、余数只可能有0 、1、 2、 3、 4、 5、 6、 7、 8、 9、 10这11个数字。其分别对应的最后一位身份证的号码为1 .0. X. 9. 8. 7. 6. 5. 4. 3. 2.。
        5、通过上面得知如果余数是2，就会在身份证的第18位数字上出现罗马数字的Ⅹ。如果余数是10，身份证的最后一位号码就是2。

        :return: 18位身份证号码
        :rtype: str
        """
        if len(self.id) == 15:
            digital_ontology_code = self.id[0:6] + '19' + self.id[6:15]
            return digital_ontology_code + self.get_checkcode(digital_ontology_code)
        else:
            return "ERROR"

    def eighteen_to_fifteen(self) -> str:
        """
        18位身份证转15位身份证
        :return: 15位身份证
        :rtype: str
        """
        if len(self.id) == 18:
            # 去掉第6，7位和第18位即可18位身份证转15位身份证
            return self.id[0:6] + self.id[8:17]
        else:
            return "ERROR"

    @classmethod
    def verify_id(cls, id_card_number):
        """校验身份证是否正确"""
        if not re.match(area.ID_NUMBER_18_REGEX, id_card_number):
            return bool(re.match(area.ID_NUMBER_15_REGEX, id_card_number))
        else:
            check_digit = cls(id_card_number).get_check_digit()
            return str(check_digit) == id_card_number[-1]

    @classmethod
    def fake_id(cls, sex:[0,1]=0,area_number=0):
        """
        随机生成身份证号，sex = 0表示女性，sex = 1表示男性
        生日在1960-2010区间
        """
        if int(area_number) not in area.AREA_INFO.keys():
            # 随机生成一个区域码(6位数)
            id_card_number = str(random.choice(list(area.AREA_INFO.keys())))
        else:
            # 指定区域码
            id_card_number = area_number
        # 限定出生日期范围(8位数)
        start, end = datetime.strptime("1960-01-01", "%Y-%m-%d"), datetime.strptime("2010-12-31", "%Y-%m-%d")
        birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
        id_card_number += str(birth_days)
        # 顺序码(2位数)
        id_card_number += str(random.randint(10, 99))
        # 性别码(1位数)
        id_card_number += str(random.randrange(sex, 10, step=2))
        # 校验码(1位数)
        return id_card_number + str(cls(id_card_number).get_check_digit())


def write_info(data):
    for message in data:
        with open('people_number.txt','a+',encoding="utf-8") as f:
            f.write(message+'\n')



if __name__ == '__main__':
    title()
    address = input("请输入要查找的区域(eg:北京市海淀区):")
    print("区域码 城市")
    for key,value in area.AREA_INFO.items():
        if address in value:
            print(key,value)
    random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
    area_number =input("请输入要生成的城市区域码：")
    number = int(input("请输入要生成的身份证数量："))
    i = 0
    result = set()
    while(i < number):
        print("[-]正在生成中....")
        people_number = IdCardNumber.fake_id(random_sex,area_number)  # 随机生成身份证号
        verify_stat = IdCardNumber.verify_id(people_number) # 检验身份证是否正确:
        if verify_stat:
            i = i+1
            result.add(people_number)

    write_info(result)
    print("[+]生成成功！结果保存在脚本所在目录下的people_number.txt 中")

