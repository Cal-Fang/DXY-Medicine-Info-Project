Python 3.0 or more advanced version required.

SCRAPING DATA
Step 1: getIP.py will acquire some proxy IPs for the scraping work. [100 IP per time]

Step 2: testIP.py will test the effectiveness of acquired proxy IPs.
        effective IPs will be stored in the goodIP.txt file.
        
Step 3: medicalSpider.py will scrape medicine info from the target website (http://drugs.dxy.cn).
        Two funcition inclueded (better run them one by one):
        a. step0()
            generate temp.txt, which consist of "url + China Approved Drug Names (CADN) + Factories + Trade Name".
            Information acquired through this function is insignificant. So there is no anti-spider program. 
        b. step1()
            generate temp2.txt，which consist of "CADN + Trade Name + Ingredient + Use".
            Since there are some specific information acquired through this function, although I used proxy IPs and random User-Agent and slowed down the speed. It still got blocked sometimes. When running into such block, it will report error like:
            
                                      Traceback (most recent call last):
                                        File "medicalSpider.py", line 185, in <module>
                                          step1() #得到temp2.txt,为药物名+商品名+成份+适应症
                                        File "medicalSpider.py", line 171, in step1
                                          raw_data = parseHtml2(getHtml(u, url))
                                        File "medicalSpider.py", line 59, in parseHtml2
                                          return raw_result[0]
                                      IndexError: list index out of range
                                      
             That is because it return the captcha page. Captcha page will be stored in the error.html. When reporting this error, we could just open the page in error.html with browser and type in the captcha by hand. (Change to another group of IP will be suggested.) It will restart from the broken address, so there will be no duplicated info.

Step 4: dataHandle.py will clean the data and transform it to json file.
        a. generate data0.txt and data1.txt
            remove the duplicate info from temp.txt and temp2.txt (since some medicine could be put into several categories)
        b. generate data2.txt
            intergrate data0.txt and data1.txt. The basic rule is if both name and trade name are same, they will be treated 
            as one medicine, but there will be several variable in the factories and url column, which means these several 
            company are producing a same medicine.
        c. generate data3.txt
            remove the NaN info and dupilicate info.
        d. generate the data.json from data3.txt. It will look like:
            {"name":"卡维地洛片", "tradeName":"妥尔", "ingredient":"本品主要成份为卡维地洛。", "use":"轻-中度原发性高血压。",  
                      "factories":["海南碧凯药业有限公司"], "url":["http://drugs.dxy.cn/drug/115489.htm"]}

P.S. There are some webpages' format different from the normal format, which resulted in some abnormal record. Step 4 will stop when run into these abnormal records, and you could revise the format by hand or delete it and then contiune the program. After such revision, I got some result saved as data4.txt, for your reference.



ANALYZING DATA
I havn't done it since I got another final to prepare for =D
But I was considering obtaining the income and profit information of the drug companies listed here, maybe through some industry database or scraping from some other publication platform. And then we could check whether there are any correlation between the amount of medicine produced, the use of medicine produced, and the profitability or other management index. We could also check the difference between generic medicine and patent medicine.

Anyway, that's it. I might come back to this after my accounting final =D Let me know if you think this is interesting!
