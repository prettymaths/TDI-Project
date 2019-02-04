# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:14:23 2018
Use the skuid pool generated in all categories and scrape prices and time through the API interface
@author: lan
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

#MacbookPro_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
#IPhone6_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

# get response from url address
# if not responting, wait for 2 seconds and try <=3 times
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


def getallskuid_fromlist(ClassL2,cateL2list):
    idset_all=[]
    for icateL2list in cateL2list:
        cateL1, cateL2, cateL2name,cateurl=ClassL2[icateL2list]
        f=open('item_skuid_'+str(cateL1)+'-'+str(cateL2)+'-'+cateL2name+'.pckl','rb')
        idset=pickle.load(f)
        idset_all.extend(idset)    
    idset_all=list(set(idset_all))
    return idset_all


def item_price_scrape(idsetall,savename):
    item_price_info=[]
    count=0
    for skuid in idsetall:
        #search price based on skuid
        for attempt in range(11):
            priceurl = get_urlresult('http://p.3.cn/prices/get?skuid=J_'+skuid)
            price= re.findall('\"p\":\"(.*?)\"',str(priceurl))
            if price!=[]:
                break
            elif price==[] and attempt!=9:
                time.sleep(11)
            elif attempt==9:
                price=[-1]
                print('Fail to get price for_'+str(skuid))

        item_price_info.append([str(skuid),float(price[0]),time.strftime('%Y-%m-%d %H:%M:%S')])
        time.sleep(11)
        
        if len(item_price_info)%1000==0:
            # save as lists
            print('Saving 1000*'+str(count)+savename)
            f=open(savename+'.pckl','wb')
            pickle.dump(item_price_info,f)
            f.close()
            count+=1           
    
            item_price_info_df=pd.DataFrame(item_price_info)
            item_price_info_df.to_csv(savename+'.csv')
    print('Done scraping prices_', savename)
    
#########################################################################
#f=open('CateL1L2.pckl','rb')
#[ClassL1,ClassL2]=pickle.load(f)
#for cateL2list in list(range(760,860)):
#    skuidsetall=getallskuid_fromlist(ClassL2,[cateL2list])
#    cateL1, cateL2, cateL2name,caturl=ClassL2[cateL2list]
#    savename='item_price_'+str(cateL1)+'-'+str(cateL2)+'-'+cateL2name+'-'
#    item_price(skuidsetall,savename)

# or establish a price library for all the skuids
f=open('CateL1L2.pckl','rb')
[ClassL1,ClassL2]=pickle.load(f)
# for books- cat38, ebboks-cat40
cateL2list=[]
cateL1list=[38,40]
for ind in range(len(ClassL2)):
    if (ClassL2[ind][0] in cateL1list):
        cateL2list.append(ind) 

skuidsetall=getallskuid_fromlist(ClassL2,cateL2list)
savename='item_price_books'
#item_price_srape(skuidsetall,savename)
idsetall=skuidsetall
item_price_info=[]
count=0; currentcount=0
idscraped=[]
idtoscrape=idsetall.copy()

#########################################################################################
item_price_info=[]
count=9; currentcount=0
savename='item_price_books'
f=open('item_skuid_all_price_toscrape.pckl','rb')
[idsetall,idtoscrape,idscraped]=pickle.load(f)

while len(idtoscrape)!=[]:
    try:
        for skuid in idtoscrape:
            #search price based on skuid
            for attempt in range(11):
                priceurl = get_urlresult('http://p.3.cn/prices/get?skuid=J_'+skuid)
                price= re.findall('\"p\":\"(.*?)\"',str(priceurl))
                if price!=[]:
                    break
                elif price==[] and attempt!=9:
                    time.sleep(11)
                elif attempt==9:
                    price=[-1]
                    print('Fail to get price for_'+str(skuid))

            item_price_info.append([str(skuid),float(price[0]),time.strftime('%Y-%m-%d %H:%M:%S')])
            time.sleep(11)
            currentcount=currentcount+1
            idscraped.append(skuid)
            idtoscrape.remove(skuid)
                
            if currentcount>1000:
                # save as lists
                print('Saving 1000*'+str(count)+savename)
                f=open(savename+'_'+str(count)+'x1000'+'.pckl','wb')
                pickle.dump(item_price_info,f)
                f.close()
    
                item_price_info_df=pd.DataFrame(item_price_info)
                item_price_info_df.to_csv(savename+'_'+str(count)+'x1000'+'.csv')
            
                f=open('item_skuid_all_price_toscrape.pckl','wb')
                pickle.dump([idsetall,idtoscrape,idscraped],f)
                f.close() 
            
                count+=1
                currentcount=0

    except:
                print('Not complete 1000*'+str(count)+savename)
                f=open(savename+'_'+str(count)+'x1000_notcomplete'+'.pckl','wb')
                pickle.dump(item_price_info,f)
                f.close()
    
                item_price_info_df=pd.DataFrame(item_price_info)
                item_price_info_df.to_csv(savename+'_'+str(count)+'x1000_notcomplete'+'.csv')
                
                f=open('item_skuid_all_price_toscrape.pckl','wb')
                pickle.dump([idsetall,idtoscrape,idscraped],f)
                f.close()
                count+=1
                currentcount=0
                time.sleep(6000)
    
print('Done scraping prices!')
