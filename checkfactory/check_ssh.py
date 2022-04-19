import prometheus_client
from prometheus_client import Counter, Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import paramiko
import threading
import datetime
import time
import random
from multiprocessing.dummy import Pool as ThreadPool

app = Flask(__name__)
with open('host.txt', 'r', encoding='UTF-8') as f:
    class_names = f.readlines()
hosts = [c.strip() for c in class_names]
print("远程主机为：%s \n" % hosts)

# 返回多个metrics,定义一个仓库，存放数据
REGISTRY = CollectorRegistry(auto_describe=False)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def check_ssh(item):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    cmd = "echo 【%s】 login from prometheus >>/home/inssa/login.txt" % now_time
    aaa = Gauge("H" + str(item).replace(".", "_"), "ssh stats is:", registry=REGISTRY)
    try:
        ssh.connect(hostname=item, port=9022, username='inssa', password='fz40t:oNQj', timeout=2)
        stdout = ssh.exec_command(cmd)
        ssh.close()
        print("%s ssh登录成功" % item)

        with open("ok.txt", 'a') as ok:
            ok.write("【%s】host %s ok\n" % (now_time, item))
        aaa.set(1)
    except Exception as e:
        with open("fail.txt", 'a') as ok:
            ok.write("【%s】host %s failed\n" % (now_time, item))
        print("%s ssh登录失败，失败原因：%s" % (item, e))
        aaa.set(0)


pool = ThreadPool()
pool.map(check_ssh, hosts)
pool.close()
pool.join()


# @app.route("/metrics")
# def ApiResponse():
#     print("REGISTRY", REGISTRY)
#     pool = ThreadPool()
#     pool.map(check_ssh, hosts)
#     pool.close()
#     pool.join()
#     return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True, port=9000)
