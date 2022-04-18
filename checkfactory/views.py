import requests
import datetime
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# class check_factory:
#     def __init__(self):
#         pass

url_list = ['https://10.17.110.100', 'https://10.47.1.110', 'https://10.70.100.30', 'https://10.12.3.17',
            'https://10.15.1.156', 'https://10.68.2.30', 'https://10.37.100.50', 'https://10.21.1.60',
            'https://10.63.102.90', 'https://10.33.8.2', 'https://10.10.153.253', 'https://10.64.1.206',
            'https://10.9.100.91', 'https://10.1.9.45']

dict_factory = {'红磷': 'https://10.17.110.100', '青海': 'https://10.47.1.110', '盛宏': 'https://10.70.100.30',
                'CPIC': 'https://10.12.3.17', '天聚': 'https://10.15.1.156', '大为': 'https://10.68.2.30',
                '云峰': 'https://10.37.100.50', '三环': 'https://10.21.1.60', '石化': 'https://10.63.102.90',
                '天安': 'https://10.33.8.2', '水富': 'https://10.10.153.253', '大地': 'https://10.64.1.206',
                '金新': 'https://10.9.100.91', '集团': 'https://10.1.9.45', '态感': 'https://10.1.2.178'}


def get_code():
    log = open("./log.txt", "a")
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    log.write("================================== %s ===========================================\n" % now_time)
    for i in dict_factory:
        try:
            response = requests.get(dict_factory[i], verify=False, timeout=2)
            http_code = response.status_code

            if str(http_code) == "200":
                print(i, " 状态正常 ", "返回码为", http_code)
                log.write(i + " 状态正常 " + " 返回码为" + str(http_code) + '\n')
                # with open("./ok.txt", 'a') as log:

            else:
                print(i, " 状态异常 ", "返回码为", str(http_code))
                log.write(i + " 状态异常 ???????????????????????" + '\n')
                # with open("./ok.txt", 'a') as log:
        except Exception as e:
            print(i, " 连接超时 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            log.write(i + " 连接超时 " + "???????????????????????" + '\n')
            # with open("./ok.txt", 'a') as log:

    log.close()


get_code()
