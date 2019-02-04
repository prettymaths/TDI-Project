# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:14:23 2018
Use the skuid pool generated in all categories and scrape prices and time through the API interface
Books category only
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

##30441340; 12450851
def get_item_info(currentskuid):
    item_url='https://item.jd.com/'+str(currentskuid)+'.html'
    item=str(get_urlresult(item_url))
    
    venderId=re.findall('venderId:(\S*?)\,',item)
    if venderId!=[]:
        venderId=venderId[0].replace('\'','').replace('\"','')
    else:
        venderId='0'
    shopId=re.findall('shopId:(\S*?),',item)
    if shopId!=[]:
        shopId=shopId[0].replace('\'','').replace('\"','')
    else:
        shopId='0'
    # special attributes
    temp=re.findall('isEBook:(\S*?),',item)
    if temp!=[]:
        isebook=1 if temp=='true' else 0
    else: isebook=0
    
    temp=re.findall('specialAttrs\:\[(.*?)\]',item)
    if temp!=[]:
        specialattr=temp[0].replace('\"','').replace('\'','').split(',')
        specialattr=list(zip(specialattr,'1'*len(specialattr)))
    else:
        specialattr=[]
    
    # pick subtypes
    temp=re.findall('colorSize:\ \[(.*)\]',item)
    # extract skuid
    skuid=re.findall('\"skuId\"\:(\S+?)[\,\}]',str(temp))
    skuid.extend(re.findall('\"SkuId\"\:(\S+?)[\,\}]',str(temp)))
    if skuid==[]:
       skuid=[currentskuid]
    
    item_info=[]
    for ielement in range(len(skuid)):
        subitem = get_urlresult('https://item.jd.com/'+skuid[ielement]+'.html',BS=0)
        subitem2 =BeautifulSoup(subitem,'lxml')
        
        #book name
        attr0_valuename=re.findall('name\:.?\'(\S*?)\'',subitem)
        
        if attr0_valuename!=[]:
                if '/u' in attr0_valuename[0] or '\\u' in attr0_valuename[0]:
                    tempname=attr0_valuename[0].encode('utf-8').decode('unicode_escape')
                else:
                    tempname=attr0_valuename[0]
                bookname=(tempname.replace('/','-').replace('\\','').replace('\'',''))
        else:
            bookname='NA'
        # author name, if available
        author='NA'
        attr1_valuename=re.findall('authors\:.?\[(.*?)\]',subitem)
        if attr1_valuename!=[]:
            author=attr1_valuename[0].replace('\"','').replace('\'','')
        else:
            temp=subitem2.find_all('div',class_='author')
            attr1_valuename=re.findall('\>(.*?)\<\/a\>',str(temp))
            author='='.join(attr1_valuename)
        
        #other attributes
        attr2_valuename=re.findall('title\=.*?\>(.*?)\：(.*?)\<',subitem)
        if attr2_valuename!=[]:
            bookinfo=[(x[0].replace(' ','').replace('\u3000',''),x[1].replace(' ','').replace('\u3000','')) for x in attr2_valuename]
        else:
            temp=subitem2.find_all('div', class_="bookInfo")
            attr2_valuename=re.findall('dt\"\>(.*?)\<\/div\>\n.*?dd\"\>(.*?)\<',str(temp))
            temp=subitem2.find_all('div', class_="publishing li")
            attr2_valuename.extend(re.findall('dt\"\>(.*?)\<\/div\>\n.*?dd\"\>\n.*?\>(.*?)\<',str(temp)))
            bookinfo=[(x[0].replace(' ','').replace('\u3000',''),x[1].replace(' ','').replace('\u3000','')) for x in attr2_valuename]
                
        #book category
        attr3_valuename=re.findall('cat\:.*?\[(.*?)\,(.*?)\,(.*?)\]',subitem)
        if attr3_valuename!=[]:
            bookcat=str(attr3_valuename[0]).replace('(','').replace(')','').replace('\'','').split(',')
        else:
            bookcat=['NA','NA','NA']
        #book category name
        attr4_valuename=re.findall('catName\:.*?\[(.*?)\,(.*?)\,(.*?)\]',subitem)
        if attr4_valuename!=[]:
            bookcatname=[x.replace('\"','').replace(' ','').replace('\u3000','') for x in attr4_valuename[0]]
        else:
            temp=subitem2.find_all('div', class_="category li")
            bookcatname=re.findall('\>(.*?)\<\/a\>',str(temp))
        if bookcatname==[]:
            bookcatname=['NA','NA','NA']
        
        #combine all information into a dictionary
        info=dict(BookName=bookname,Author=author); info.update(bookinfo);
        info.update(Cate0=bookcat[0],Cate1=bookcat[1],Cate2=bookcat[2],CateN0=bookcatname[0],CateN1=bookcatname[1],CateN2=bookcatname[2])
        info.update(skuId=skuid[ielement],venderId=venderId,shopId=shopId,\
                    isEbook=isebook,ScrapeTime=time.strftime('%Y-%m-%d %H:%M:%S'))
        info.update(specialattr)

        item_info.append(info)
        time.sleep(2)   
    
    # append shop evaluation
    ipage=0;
    commenturl = r'http://club.jd.com/productpage/p-{}-s-0-t-3-p-{}.html'.format(skuid[0],ipage)
    
    try:
         comment = json.loads(get_urlresult(commenturl,BS=0))
    except:
         comment='error'
    
    # extract general comments to these items, join to each subitem
    try:
        if comment!='error':
            generalinfo={key: comment['productCommentSummary'][key] for key in ['averageScore','commentCount',\
                 'generalCount','goodCount','poorCount','afterCount','showCount','skuId'] }
            generalinfo['skuId_father']=generalinfo.pop('skuId')
        else:
            generalinfo={}
    except:
        generalinfo={}
    for ielement in range(len(skuid)):
        item_info[ielement].update(generalinfo)

    return item_info,skuid
        

def item_info_scrape(idsetall,savename):
    item_info=[]
    count=0
    idtoscrape=idsetall.copy()
    idscraped=[]
    while idtoscrape!=[]:
        currentid=idtoscrape[0]        
        item_info_temp,temp_iddone=get_item_info(currentid)
        idscraped.extend(temp_iddone)
        if temp_iddone!=[]:
            item_info.extend(item_info_temp)
            # add new skuid into the set and delete processed skuids from the set
            for tempid in temp_iddone:
                if tempid in idtoscrape:
                    idtoscrape.remove(tempid)
                if tempid not in idsetall:
                    idsetall.append(tempid)
        else:
            idtoscrape.remove(currentid)
        
        #save to file every 1000 items
        if len(idscraped)%1000==0:
            print('Saving info_'+str(count*1000)+'_outtof_'+str(len(idsetall)))
            f=open(savename+'_'+str(count)+'x1000.pckl','wb')
            pickle.dump(item_info,f)
            f.close()
            count+=1
            
            item_info_df=pd.DataFrame(item_info)
            item_info_df.to_csv(savename+'_'+str(count)+'x1000.csv',encoding="utf-8-sig")
            item_info=[]
    
            # update_skuid
            f=open('item_skuid_all_toscrape.pckl','wb')
            pickle.dump([idsetall,idtoscrape],f)
            f.close()
    
    return idsetall,idtoscrape,idscraped

######################################################################################
f=open('CateL1L2.pckl','rb')
[ClassL1,ClassL2]=pickle.load(f)
# for books- cat38, ebboks-cat40
cateL2list=[]
cateL1list=[38,40]
for ind in range(len(ClassL2)):
    if (ClassL2[ind][0] in cateL1list):
        cateL2list.append(ind)

skuidsetall=getallskuid_fromlist(ClassL2,cateL2list)
savename='item_info_books'
#item_info_scrape(skuidsetall,savename)

idsetall=skuidsetall
item_info=[]
count=0; currentcount=0
idtoscrape=idsetall.copy()
idscraped=[]
#######################################################################################
savename='item_info_books'
f=open('item_skuid_all_toscrape.pckl','rb')
[idsetall,idtoscrape,idscraped]=pickle.load(f)
item_info=[]
count=953; currentcount=0
while idtoscrape!=[]:
    try:
        currentid=idtoscrape[0]
        item_info_temp,temp_iddone=get_item_info(currentid)
        if currentid not in temp_iddone:
            temp_iddone.append(currentid)
        if temp_iddone!=[]:
            item_info.extend(item_info_temp)
            idscraped.extend(temp_iddone)
            # add new skuid into the set and delete processed skuids from the set
            for tempid in temp_iddone:
                if tempid in idtoscrape:
                    idtoscrape.remove(tempid)
                if tempid not in idsetall:
                    idsetall.append(tempid)
        else:
            idtoscrape.remove(currentid)
            idscraped.extend(currentid)
        
        currentcount=currentcount+len(temp_iddone)
        #save to file every 1000 items
        if currentcount>1000:
            print('Saving info_'+str(count*1000)+'_outtof_'+str(len(idsetall)))
            f=open(savename+'_'+str(count)+'x1000.pckl','wb')
            pickle.dump(item_info,f)
            f.close()
          
            item_info_df=pd.DataFrame(item_info)
            item_info_df.to_csv(savename+'_'+str(count)+'x1000.csv',encoding="utf-8-sig")
            item_info=[]

            count+=1
            currentcount=0
            # update_skuid
            f=open('item_skuid_all_toscrape.pckl','wb')
            pickle.dump([idsetall,idtoscrape,idscraped],f)
            f.close()
    except:
            print('Not complete info_'+str(count*1000)+'_outtof_'+str(len(idsetall)))
            f=open(savename+'_'+str(count)+'x1000_notcomplete.pckl','wb')
            pickle.dump(item_info,f)
            f.close()
          
            item_info_df=pd.DataFrame(item_info)
            item_info_df.to_csv(savename+'_'+str(count)+'x1000_notcomplete.csv',encoding="utf-8-sig")
            item_info=[]

            count+=1
            currentcount=0
            # update_skuid
            f=open('item_skuid_all_toscrape.pckl','wb')
            pickle.dump([idsetall,idtoscrape,idscraped],f)
            f.close()
            time.sleep(6000)
        
print("Done Scraping"+savename)
