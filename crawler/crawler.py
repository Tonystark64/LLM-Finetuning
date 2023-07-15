import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import pandas as pd
import numpy as np
from lxml import etree
import urllib
import urllib3
import time
import random
import argparse
import datetime
import os

def SinglePage(url, headers, out, themeID, startP, endP, curP,proxies={}):
    home = "/".join(url.split('/')[:3])
    # requests.adapters.DEFAULT_RETRIES = 1
    re_try_times = 3
    while re_try_times:
        try:
            html = requests.get(url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(html.text, 'lxml')
            titles = soup.find_all('a', attrs={'class': 'xst'})
            if (len(titles) >= 1):
                break
        except Exception as e:
            print(e)
            print("%s connection failed: retrying..."%(url))
            time.sleep(2)
            if (re_try_times==0):
                return
        re_try_times -= 1
    selector = etree.HTML(html.text)
    theme = selector.xpath("/html/body/div[15]/div/div[2]/div[2]/div[2]/div[3]/div[2]/a[3]")  
    theme = theme[0].text
    print("themeID:",themeID,"-","currentPage:",curP,"-",titles[0].get_text()[:15])           
    dict1 = {'theme':[],'title':[], 'href':[]}
    for title in titles:
        try:
            SingleTitle(home + "/" + title.get('href'), out, themeID, startP,\
                        endP, curP, title.get_text(), theme,proxies=proxies)
        except Exception as e:
            print(e)
            continue
        time.sleep(10)
        # print(title.get_text())

def SingleTitle(url, out, themeID, startP, endP, curP, \
                title="边度有channel卖", theme='潮流时尚', proxies={}):
    global global_counter
    '''
    requests.adapters.DEFAULT_RETRIES = 1
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 \
               Safari/537.36",
               'Referer':parentURL,
               'Host':'https://www.baby-kingdom.com',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Accept-Encoding':'gzip, deflate, br',
               'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Connection':'keep-alive',
               'cache-control':'max-age=0',
               'Cookie':'rAvd_2132_lastact=1689322923%09forum.php%09viewthread; rAvd_2132_lastvisit=1689318055; rAvd_2132_oldtopics=D23661500D23674973D; rAvd_2132_sid=UuRkka; rAvd_2132_visitedfid=965D162'
               }
    '''
    html = requests.get(url, headers={'User-Agent':random.choice(my_headers)}, proxies=proxies)
    cycle = "/html/body/div[12]/div[1]/div[2]/div[2]/div[2]/div[10]/div[1]/div/div[1]/div[2]/div[1]/"
    selector = etree.HTML(html.text)
    timeTable = []
    times = selector.xpath(cycle + "/div[2]/div[1]/div[2]/em[1]/span[1]")
    if (len(times) < 1):
        return
    timeTable.append(times[0].text)
    subTimes = selector.xpath(cycle + "/div[1]/div[1]/div[2]/em[1]/span[1]")
    for subTime in subTimes:
        timeTable.append(subTime.text)
    view = selector.xpath("/html/body/div[12]/div[1]/div[2]/div[2]/div[2]/div[10]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]")
    view = view[0].text.replace("查看:","").strip()
    reply = selector.xpath("/html/body/div[12]/div[1]/div[2]/div[2]/div[2]/div[10]/div[1]/div[1]/div[1]/div[1]/div[1]/span[3]")
    reply = reply[0].text.replace("回覆:","").strip()
    share = selector.xpath("/html/body/div[12]/div[1]/div[2]/div[2]/div[2]/div[10]/div[1]/div[4]/div[1]/div[2]/div[2]/div[1]/a[1]/span[1]/span[1]")
    share = share[0].text
    support = selector.xpath("/html/body/div[12]/div[1]/div[2]/div[2]/div[2]/div[10]/div[1]/div[4]/div[1]/div[2]/div[2]/div[1]/a[2]/span[1]/span[1]")
    support = support[0].text
    oppose = selector.xpath("/html/body/div[12]/div[1]/div[2]/div[2]/div[2]/div[10]/div[1]/div[4]/div[1]/div[2]/div[2]/div[1]/a[3]/span[1]/span[1]")
    oppose = oppose[0].text
    soup = BeautifulSoup(html.text, 'lxml')
    posts = soup.find_all(attrs={'id':re.compile(r'^postmessage_')})
    quotes = soup.find_all(attrs={'class':'quote'})
    strong = soup.find_all('strong')
    pstatus = soup.find_all(attrs={'class':'pstatus'})
    strong = [i for i in strong if '回覆' in i.text[:2]]
    del1 = 0
    del2 = 0
    del3 = 0
    counter = 0
    dict1 = {'theme':[],'title':[],'url':[],'post':[],'time':[],'view':[],'reply':[],'share':[],'support':[],'oppose':[]}
    for po in posts:
        newPo = po.text
        if del1 < len(quotes) and quotes[del1].text in po.text:
            newPo = po.text.replace(quotes[del1].text.strip(),"")
            del1+=1
        elif del2 < len(strong) and strong[del2].text in po.text:
            newPo = po.text.replace(strong[del2].text.strip(),"")
            del2+=1
        elif del3 < len(pstatus) and pstatus[del3].text in po.text:
            newPo = po.text.replace(pstatus[del3].text.strip(),"")
            del3+=1
        newPo = newPo[:newPo.find("googletag.cmd.push")]
        newPo = newPo[:newPo.find("\n\n\n\n")]
        if newPo.find("本帖最後由") != -1:
            newPo = newPo[newPo.find("編輯")+3:]
        newPo = newPo.strip()
        dict1['theme'].append(theme)
        dict1['title'].append(title)
        dict1['url'].append(url)
        dict1['post'].append(newPo)
        dict1['time'].append(timeTable[counter])
        dict1['view'].append(view)
        dict1['reply'].append(reply)
        dict1['share'].append(share)
        dict1['support'].append(support)
        dict1['oppose'].append(oppose)
        counter+=1
        global_counter += 1
    print("themeID:",themeID,"-","currentPage:",curP,"-lastPost:",newPo[:15])
    df1 = pd.DataFrame(dict1)
    # curTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # : is not allowed in csv file
    fileName = "theme_"+str(themeID)+"_start" + str(startP) + "_end" + str(endP) + ".csv"
    path1 = os.path.join(out, fileName)
    if os.path.exists(path1):
        # print('old file')
        df1.to_csv(path1,mode='a',index=False,header=False)
    else:
        # print('new file')
        df1.to_csv(path1,index=False)
    
def urlGen(themeID, pageID):
    url = "https://www.baby-kingdom.com/forum.php?mod=forumdisplay&fid="
    url += str(themeID)
    url += "&page="
    url += str(pageID)
    return url

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
proxies={
    #"http":"http://58.20.184.187:9091",
    "http":"http://60.182.184.172:8888",
    #"http":"http://111.3.102.207:30001"
}

global_counter = 0

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--themeID', type=int, default=965)
    parser.add_argument('--startPage', type=int, default=21)
    parser.add_argument('--endPage', type=int, default=23)
    parser.add_argument('--output_path',type=str, required=True)
    args = parser.parse_args()
    
    global_counter = 0

    # output_path='D:\\22_23Term2\\IEMS5930\\ART350\\爬虫学习'

    headers = {'User-Agent':random.choice(my_headers)}
    
    start_time = time.time()
    
    for page in range(args.startPage,args.endPage+1):
        url = urlGen(args.themeID, page)
        try:
            print("theme_ID:%d page:%d started:"%(args.themeID,page))
            SinglePage(url, headers=headers, out = args.output_path, \
                       themeID=args.themeID, startP=args.startPage,\
                        endP=args.endPage,curP=page,proxies=proxies)
        except Exception as e:
            print(e)
            continue
        print("theme_ID:%d page:%d finished"%(args.themeID,page))
        time.sleep(2)

    fileName = "theme_"+str(args.themeID)+"_start" + str(args.startPage) + "_end" + str(args.endPage) + ".csv"
    print("total time cost: %d s"%(time.time()-start_time))
    dict_print = {"file_name":fileName,"entry_number":global_counter,"time_cost(s)":time.time()-start_time}
    df_print = pd.DataFrame(dict_print)
    if os.path.exists("records.csv"):
        df_print.to_csv("records.csv",mode='a',index=False,header=False)
    else:
        df_print.to_csv("records.csv",index=False)



