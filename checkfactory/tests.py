#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from flask import Flask, Response
from prometheus_client import Counter, generate_latest, Gauge
from prometheus_client.core import CollectorRegistry, Histogram
import paramiko
import test2

app = Flask(__name__)

registry = CollectorRegistry()
g = Gauge('ssh_contact', 'an example showed how to use gauge', ['machine_ip'], registry=registry)

with open('host.txt', 'r', encoding='UTF-8') as f:
    class_names = f.readlines()
hosts = [c.strip() for c in class_names]
print("远程主机为：%s \n" % hosts)


@app.route('/metrics')
def hello():
    start_time = time.time()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host_ssh_dict = test2.get_data()
    print("host_ssh_dict", host_ssh_dict)
    for key, value in host_ssh_dict.items():
        g.labels(key).set(value)
    end_time = time.time()
    print("cost:", end_time - start_time)
    return Response(generate_latest(g), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
