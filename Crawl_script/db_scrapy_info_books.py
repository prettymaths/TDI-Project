# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 22:13:04 2019

@author: prettymaths
"""
from bs4 import BeautifulSoup
import requests
import time
import re
import json
import pickle
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import pandas as pd
import random
import urllib

def get_urlresult(url,BS=1):
    useragent=\
    ['Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1']
    
    headers={'User-Agent':useragent[random.randint(0,len(useragent)-1)]}
    for attempt in range(10):
        try:
            request = requests.get(url,headers)
            if BS==1:
                result=BeautifulSoup(request.text,'lxml')
            elif BS==0:
                result=request.text          
            
            if result!='':
                return result
            elif result=='' and  attempt!=9:
                time.sleep(10)
                continue
            else:
                print('Fail to get url')
                return 0
        
        except Exception:
            if attempt==9:
                print('Fail to get url')
            time.sleep(10)
            continue    
    return 0


#%%
f=open('isbn_scraped.pckl','rb')
isbn_list=pickle.load(f)
bookcomment=[]
count=1
isbn_list=list(isbn_list)
iisbn=0;
#%%

f=open('bookcomment.pckl','rb')
[iisbn,isbn_list,count,bookcomment]=pickle.load(f)
iisbn=iisbn+1
while iisbn<len(isbn_list):
        url='https://api.douban.com/v2/book/isbn/'+isbn_list[iisbn]
        response = get_urlresult(url,BS=0)
        if "rating" in response:
            response = json.loads(response)
            # convert review rating and tags (lists) to individual columns
            temp=response['rating']
            response['numRaters']=temp['numRaters']
            if response['numRaters']>2:
                response['avgrating']=temp['average']
                response['maxrating']=temp['max']
                response['minrating']=temp['min']
            del response['rating']
                
            temp=response['tags']
            for itag in range(len(temp)):
                response['tag'+str(itag)]=temp[itag]['name']
                response['tagcount'+str(itag)]=temp[itag]['count']
            del response['tags']
            
            # get the book image url, download and save
            response['imageurl']=response['images']['large']
            del response['images']
            del response['image']
            
            time.sleep(5)
            for attempt in range(5):
                try:
                    urllib.request.urlretrieve(response['imageurl'],isbn_list[iisbn]+'.jpg')
                    break
                    time.sleep(2)
                except:
                    time.sleep(10)      
                    attempt=attempt+1
                
            bookcomment.append(response)
            #time.sleep(11)
        elif "code" in response:
            response = json.loads(response)
            if response['code']==112:
                print('RateExceedLimit iisbn='+str(iisbn))
                iisbn=max(iisbn-1,0)
                f=open('bookcomment.pckl','wb')
                pickle.dump([iisbn,isbn_list,count,bookcomment],f)
                f.close() 
                time.sleep(600)
            elif response['code']==6000:
                response={}
                response['isbn13']=isbn_list[iisbn]
                response['Error']=1
                print('NA ISBN')
                time.sleep(5)
                bookcomment.append(response)
        
        if iisbn>1000*count:           
            f=open('bookcomment.pckl','wb')
            pickle.dump([iisbn,isbn_list,count,bookcomment],f)
            f.close()
            print('Done iisbn='+str(iisbn))
            count=count+1
        
        iisbn=iisbn+1
#bookcomment.to_csv('bookcomment_part1.csv',encoding="utf-8-sig")









