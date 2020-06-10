# -*- coding: utf-8 -*-
import re
from urllib import request
import time
import random
import socket
import fake_useragent

socket.setdefaulttimeout(3)
ipF = open('goodIP.txt', 'r')
ips = ipF.readlines()
ipF.close()
basicUrlHead = 'http://drugs.dxy.cn/category/'
basicUrlTail = '.htm?page='
category = ['1227', '1251', '1286', '1311', '1320', '1333', '1355', '1367', '1379']
page = [50, 28, 21, 21, 19, 10, 25, 19, 43]

def createUrl(cat, page):
    return basicUrlHead + cat + basicUrlTail + str(page)

def getHtml(url, referer = "http://drugs.dxy.cn"):
    while True:
        try:
            random_UA = fake_useragent.UserAgent().random
            req = request.Request(url)
            req.add_header("User-Agent", random_UA)
            req.add_header("Host", "drugs.dxy.cn")
            req.add_header("Referer", referer)
            req.add_header("GET", url)
            random_proxy = random.choice(ips)
            target = random_proxy.strip().split('\t')
            proxy = {target[0] : target[1]}
            proxy_support = request.ProxyHandler(proxy)
            opener = request.build_opener(proxy_support)
            return opener.open(req).read().decode("utf-8")
        except:
            ips.remove(random_proxy)
            print("retry")

def parseHtml(html):
    pattern = '<a href="http://drugs\.dxy\.cn/drug/\d+\.htm">.+?&nbsp;'
    head = '<a href="'
    results = map(lambda name : re.sub(head, '', name), re.findall(pattern, html, re.DOTALL))
    return list(results)

def parseHtml1(html):
    pattern = '<a href="http://drugs\.dxy\.cn/drug/\d+\.htm'
    head = '<a href="'
    results = map(lambda name : re.sub(head, '', name), re.findall(pattern, html, re.DOTALL))
    return list(results)

def parseHtml2(html):
    pattern = '药品名称:.+?用法用量:'
    raw_result = re.findall(pattern, html, re.DOTALL)
    if len(raw_result) == 0:
        f = open('error.html', 'w')
        f.write(html)
        f.close()
    return raw_result[0]

def cleanData(lis):
    result = []
    for msg in lis:
        want = []
        temp = ''
        for char in msg:
            if char == '\t':
                break
            temp += char
        site, name = temp.split("\">")
        want.append(site)
        want.append(name)
        factory = ''
        msg2 = msg.split(' - ')[1].strip()
        for char in msg2:
            if char == '\t':
                break
            factory += char
        want.append(factory)
        name2 = ''
        msg3 = msg.split('</b>')[-1].strip()
        for char in msg3:
            if char == '&':
                break
            name2 += char
        want.append(name2)
        result.append(want)
    return result

def cleanData2(msg):
    new_msg = ''
    flag = 0
    for i in msg:
        if i in ['\t', '\n', ' ']:
            continue
        if flag and i != '>':
            continue
        if i == '<':
            flag = 1
            continue
        if i == '>':
            flag = 0
            continue
        new_msg += i
    # print(new_msg)
    p1 = new_msg.find('通用名称')
    p2 = new_msg.find('英文名称')
    p3 = new_msg.find('商品名称')
    p4 = new_msg.find('成份')
    p5 = new_msg.find('适应症')
    p6 = new_msg.find('用法用量')
    # print(p1, p2, p3, p4, p5, p6)
    name1 = new_msg[p1 + 5 : p2]
    name2 = new_msg[p3 + 5 : p4]
    consist = new_msg[p4 + 3 : p5] 
    disease = new_msg[p5 + 4 : p6]
    p7 = disease.find('超说明书')
    if p7 != -1:
        disease = disease[:p7]
    # print(name1)
    # print(name2)
    # print(consist)
    # print(disease)
    return name1, name2, consist, disease

def step0():
    f = open('temp.txt', 'w')
    for i, cat in enumerate(category):
        print(i)
        print('---')
        for p in range(page[i]):
            print(p)
            url = createUrl(cat, p + 1)
            html = getHtml(url)
            raw = parseHtml(html)
            if p + 1 != page[i]:
                assert len(raw) == 10
            data = cleanData(raw)
            for rec in data:
                f.write(rec[0])
                f.write('\t')
                f.write(rec[1])
                f.write('\t')
                f.write(rec[2])
                f.write('\t')
                f.write(rec[3])
                f.write('\n')
    f.close()

def step1():
    f = open('temp2.txt', 'r')
    ct = len(f.readlines())
    f.close()
    f = open('temp2.txt', 'a+')
    tmp = 0
    for i, cat in enumerate(category):
        print(i)
        print('---')
        for p in range(page[i]):
            print(p)
            url = createUrl(cat, p + 1)
            html = getHtml(url)
            raw = parseHtml1(html)
            if p + 1 != page[i]:
                assert len(raw) == 10
            for u in raw:
                print(u)
                tmp += 1
                if tmp <= ct:
                    continue
                raw_data = parseHtml2(getHtml(u, url))
                rec = cleanData2(raw_data)
                f.write(rec[0])
                f.write('\t')
                f.write(rec[1])
                f.write('\t')
                f.write(rec[2])
                f.write('\t')
                f.write(rec[3])
                f.write('\n')
                time.sleep(random.randint(5, 10))
    f.close()

step0() # generate temp.txt, which consist of "url + China Approved Drug Names (CADN) + Factories + Trade Name".
step1() # generate temp2.txt，which consist of "CADN + Trade Name + Ingredient + Use".
