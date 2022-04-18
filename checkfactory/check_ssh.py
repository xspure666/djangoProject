import paramiko
import threading
import datetime
import time
from multiprocessing.dummy import Pool as ThreadPool

# hosts = ['10.17.110.100', '10.47.1.110', '10.70.100.30', '10.12.3.17', '10.15.1.156', '10.68.2.30', '10.37.100.50',
#          '10.21.1.60', '10.63.102.90', '10.33.8.2', '10.10.153.253', '10.64.1.206', '10.9.100.91', '10.1.9.45']
hosts = []
with open("host.txt") as host:
    host1 = host.read().replace("\n", "','")
    hosts.append(host1)

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# 连接服务器

# for i in hosts:
#     try:
#         ssh.connect(hostname=i, port=9022, username='inssa', password='fz40t:oNQj', timeout=2)
#     except Exception as e:
#         print("%s connect refuse===" % i)


def check_ssh(item):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    try:
        ssh.connect(hostname=item, port=9022, username='inssa', password='fz40t:oNQj', timeout=2)
        print("%s ssh登录成功" % item)
        with open("ok.txt", 'a') as ok:
            ok.write("【%s】host %s ok\n" % (now_time, item))

    except Exception as e:
        with open("fail.txt", 'a') as ok:
            ok.write("【%s】host %s failed\n" % (now_time, item))
        print("%s ssh登录失败，失败原因：" % item, e)
    # time.sleep(3)


pool = ThreadPool()
pool.map(check_ssh, hosts)
pool.close()
pool.join()

# ssh.connect(hostname='192.168.1.96', port=9022, username='inssa', password='fz40t:oNQj')
#
# cmd = 'ps'
# # cmd = 'ls -l;ifconfig'       #多个命令用;隔开
# stdin, stdout, stderr = ssh.exec_command(cmd)
#
# result = stdout.read()
#
# if not result:
#     result = stderr.read()
# ssh.close()
#
# print(result.decode())
