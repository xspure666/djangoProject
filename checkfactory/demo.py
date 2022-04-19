import paramiko
import datetime
from multiprocessing.dummy import Pool as ThreadPool

with open('host.txt', 'r', encoding='UTF-8') as f:
    class_names = f.readlines()
hosts = [c.strip() for c in class_names]

host_dict = {}


def check_ssh(item):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    cmd = "echo 【%s】 login from prometheus >>/home/inssa/login.txt" % now_time
    cmd = "uptime | awk '{print $3" " $4}'"
    try:
        ssh.connect(hostname=item, port=9022, username='inssa', password='fz40t:oNQj', timeout=10, allow_agent=False,
                    look_for_keys=False)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # print(stdout)
        # print(stdin)
        # print(stderr)
        print("%s ssh登录成功 在线时长：%s" % (item, stdout.readlines()[0]))
        # print("%s ssh登录成功 在线时长：%s" % (item, stdout))
        host_dict[item] = "1"
    except Exception as e:
        host_dict[item] = "0"
        print("%s ssh登录失败，失败原因：%s " % (item, e))
    ssh.close()


def get_data():
    pool = ThreadPool()
    pool.map(check_ssh, hosts)
    pool.close()
    pool.join()
    return host_dict


if __name__ == "__main__":
    print(get_data())
