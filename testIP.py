# -*- coding: utf-8 -*-
import os
from urllib import request
import socket
socket.setdefaulttimeout(3)
f = open('ip.txt', 'r')
lines = f.readlines()
f.close()
proxys = []
for i in range(len(lines)):
    ip = lines[i].strip().split("\t")
    proxy_host = ip[0].strip() + ":" + ip[1].strip()
    proxy_temp = {ip[2].strip().lower() : proxy_host}
    proxys.append(proxy_temp)
url = 'http://www.baidu.com'
f = open('goodIP.txt', 'w')
ct = 0
for proxy in proxys:
    ct += 1
    if ct % 100 == 0:
        print(ct)
    try:
        prox = request.ProxyHandler(proxy)
        opener = request.build_opener(prox)
        html = opener.open(url).read().decode("utf-8")
        print(proxy)
        IPtype = list(proxy.keys())[0]
        IP = list(proxy.values())[0]
        f.write(IPtype)
        f.write('\t')
        f.write(IP)
        f.write('\n')
    except:
        continue
f.close()
os.remove('ip.txt')