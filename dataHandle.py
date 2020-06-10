# -*- coding: utf-8 -*-

# Delete duplicated info
def noRepeat(filename, newname):
	f = open(filename, 'r')
	s = set(f.readlines())
	f.close()
	f = open(newname, 'w')
	f.writelines(s)
	f.close()
noRepeat("temp.txt", "data0.txt")
noRepeat("temp2.txt", "data1.txt")

# Intergrate
f = open('data1.txt', 'r')
s = f.readlines()
f.close()
f = open('data0.txt', 'r')
l = f.readlines()
f.close()
lis0 = [rec.strip().split('\t') for rec in l] #site name1 factory name2
lis1 = [rec.strip().split('\t') for rec in s] #name1 name2 ingredient use
for rec in lis1:
	assert len(rec) == 4
	for fac in lis0:
		if rec[0] == fac[1] and rec[1] == fac[3]:
			rec.append(fac[2]) #append factories
	for fac in lis0:
		if rec[0] == fac[1] and rec[1] == fac[3]:
			rec.append(fac[0]) #append links
final = ['\t'.join(rec) + '\n' for rec in lis1]
f = open('data2.txt', 'w') #name1 name2 ingredient use factories sites
f.writelines(sorted(final))
f.close()

# Delete duplicated info again
f = open('data2.txt', 'r')
lis = f.readlines()
f.close()
lis = [rec.strip().split('\t') for rec in lis] #name1 name2 ingredient use factories sites
name1, name2 = '', ''
newlis = []
for rec in lis:
	try:
		assert len(rec) > 4
	except:
		print(rec[0])
		exit(1) #无效记录请手动剔除
	if rec[0] == name1 and rec[1] == name2:
		continue
	name1, name2 = rec[0], rec[1]
	newlis.append(rec)
f = open('data3.txt', 'w')
f.writelines(['\t'.join(rec) + '\n' for rec in newlis])
f.close()

# Generate the json file
import json
#卡维地洛片	妥尔	本品主要成份为卡维地洛。	轻-中度原发性高血压。	海南碧凯药业有限公司	http://drugs.dxy.cn/drug/115489.htm
#{"name":"卡维地洛片", "tradeName":"妥尔", "ingredient":"本品主要成份为卡维地洛。", "use":"轻-中度原发性高血压。", "factories":["海南碧凯药业有限公司"], "url":["http://drugs.dxy.cn/drug/115489.htm"]}
f = open('data3.txt', 'r')
lis = f.readlines()
lis = [rec.strip().split('\t') for rec in lis] #name1 name2 ingredient use factories urls
f.close()
jsonLis = []
for rec in lis:
	dic = {}
	dic["name"], dic["tradeName"], dic["ingredient"], dic["use"] = rec[0], rec[1], rec[2], rec[3]
	dic["factories"] = []
	dic["urls"] = []
	for i in range(4, len(rec)):
		if rec[i][:4] != "http":
			dic["factories"].append(rec[i])
		else:
			dic["urls"].append(rec[i])
	jsonLis.append(dic)
f = open('data.json', 'w')
f.write(json.dumps(jsonLis, ensure_ascii = False))
f.close()
