Python 3.0 or a more advanced version is required.

SCRAPING DATA
Step 1: getIP.py will acquire some proxy IPs for the scraping work. [100 IP per time]

Step 2: testIP.py will test the effectiveness of acquired proxy IPs.
        effective IPs will be stored in the goodIP.txt file.
        
Step 3: medicalSpider.py will scrape medicine info from the target website (http://drugs.dxy.cn).
        Two functions included (better run them one by one):
        a. step0()
            generate temp.txt, which consist of "url + China Approved Drug Names (CADN) + Factories + Trade Name".
            Information acquired through this function is insignificant. So there is no anti-spider program. 
        b. step1()
            generate temp2.txt，which consist of "CADN + Trade Name + Ingredient + Use".
            Since there is some specific information acquired through this function, although I used proxy IPs and random User-Agent and slowed down the speed, it still got blocked sometimes. When running into such a block, it will report errors like:
            
                                      Traceback (most recent call last):
                                        File "medicalSpider.py", line 185, in <module>
                                          step1() #得到temp2.txt,为药物名+商品名+成份+适应症
                                        File "medicalSpider.py", line 171, in step1
                                          raw_data = parseHtml2(getHtml(u, url))
                                        File "medicalSpider.py", line 59, in parseHtml2
                                          return raw_result[0]
                                      IndexError: list index out of range
                                      
             That is because it returns the captcha page. The Captcha page will be stored in the error.html. When reporting this error, we could just open the page in error.html with the browser and type in the captcha by hand. (Change to another group of IP will be suggested.) It will restart from the broken address, so there will be no duplicated info.

Step 4: dataHandle.py will clean the data and transform it to JSON file.
        a. generate data0.txt and data1.txt
            remove the duplicate info from temp.txt and temp2.txt (since some medicine could be put into several categories)
        b. generate data2.txt
            intergrate data0.txt and data1.txt. The basic rule is if both name and trade name are the same, they will be treated as one medicine, but there will be several variables in the factories and url column, which means these several companies are producing the same medicine.
        c. generate data3.txt
            remove the NaN info and duplicate info.
        d. generate the data.json from data3.txt. It will look like:
            {"name":"卡维地洛片", "tradeName":"妥尔", "ingredient":"本品主要成份为卡维地洛。", "use":"轻-中度原发性高血压。",  
                      "factories":["海南碧凯药业有限公司"], "url":["http://drugs.dxy.cn/drug/115489.htm"]}

P.S. There are some webpages' formats different from the normal format, which resulted in some abnormal records. Step 4 will stop when run into these abnormal records, and you could revise the format by hand or delete it and then continue the program. After such revision, I got some results saved as data4.txt, for your reference.


