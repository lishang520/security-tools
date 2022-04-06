import tldextract
def title():
    print('\033[1;31m+------------------------------------------')
    print('+  安全团队:  base64-sec                           ')
    print('+      作者:  base64_painter                   ')
    print('+------------------------------------------\033[0m')
def banner():
    print('''
    结合oneforall使用：通过提取出根域名，让oneforall跑子域名，节省时间，防止重复的子域名浪费时间
    ''')
def get_main_domain(url):
    # 一级域名
    domain = tldextract.extract(url).domain
    # 二级域名
    subdomain = tldextract.extract(url).subdomain
    # 后缀
    suffix = tldextract.extract(url).suffix
    # print("获取到的一级域名:{}".format(domain))
    # print("获取到二级域名:{}".format(subdomain))
    # print("获取到的url后缀:{}".format(suffix))
    main_domain = domain+'.'+suffix
    return  main_domain
    # print(main_domain)

def write_info(data):
    with open("main_domain.txt",'a+',encoding="utf-8") as f:
        for mes in data  :
            f.write(mes+'\n')
    print("[+]结果写入完毕，在当前目录下的main_domain.txt中....")


if __name__ == '__main__':
    title()
    banner()
    results = set()
    with open('targets.txt', 'r', encoding="utf-8") as f:
        temp = f.readlines()
    print("[+]正在提取中....")
    for url in temp:
        url = url.strip()
        result = get_main_domain(url)
        results.add(result)
    print("[+]提取完毕....")
    print("[+]开始写入结果....")
    write_info(results)

