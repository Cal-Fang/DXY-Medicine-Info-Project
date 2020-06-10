# -*- coding: utf-8 -*-
import re
import random
import urllib
import fake_useragent

url = 'http://www.xicidaili.com/nn/'

def getHtml():
    header = {}
    header['User-Agent'] = fake_useragent.UserAgent().random
    page = random.randint(1, 1000)
    req = urllib.request.Request(url + str(page), headers = header)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    return res

def parseHtml(html):
    pattern1 = '<td>\d+\.\d+\.\d+\.\d+</td>'
    pattern2 = '<td>\d+</td>'
    pattern3 = '<td>HTTPS?</td>'
    head = '<td>'
    result1 = map(lambda name : re.sub(head, '', name), re.findall(pattern1, html))
    result2 = map(lambda name : re.sub(head, '', name), re.findall(pattern2, html))
    result3 = map(lambda name : re.sub(head, '', name), re.findall(pattern3, html))
    return list(result1), list(result2), list(result3)

def getIP():
    f = open('ip.txt','a')
    lis1, lis2, lis3 = parseHtml(getHtml())
    assert len(lis1) == len(lis2) == len(lis3)
    for i in range(100):
    	f.write(lis1[i][:-5])
    	f.write('\t')
    	f.write(lis2[i][:-5])
    	f.write('\t')
    	f.write(lis3[i][:-5])
    	f.write('\n')
    f.close()

getIP()