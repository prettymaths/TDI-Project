# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 11:36:54 2019
Dataset conversion and preclean
@author: prettymaths
"""
#%%
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import glob
import pickle

# load dataset and delete non-specific scraped information
filelist=glob.glob('item_info_books_*.pckl')
dataset=list()
colnames=dict()
for ifile in filelist:
    f=open(ifile,'rb')
    temp=pickle.load(f)
    dataset.extend(temp)
    for ibook in range(len(temp)):
        for ikey in temp[ibook].keys():
            if ikey in colnames:
                colnames[ikey]+=1;
            else:
                colnames[ikey]=1;

# clean dataset
colnames_clean = {k:v for k,v in colnames.items() if v >5000}
data=pd.DataFrame(dataset,columns=tuple(colnames_clean.keys()))
data.dropna(how='all',inplace=True)

# correct isbn
tmp=np.empty([data.shape[0],1])
temp=data.loc[:,'ISBN']
for iisbn in range(len(temp)):
    if (str(temp[iisbn])).isdigit()==0 or str(temp[iisbn])=='nan':
        tmp[iisbn]='nan'
    elif len(temp[iisbn])==13 and (int(temp[iisbn])>9800000000000 or int(temp[iisbn])<9780000000000):
        tmp[iisbn]='nan'
    elif (str(temp[iisbn])).isdigit()==1 and len(temp[iisbn])==10:
        tmp[iisbn]='978'+temp[iisbn]
    elif len(temp[iisbn])!=10 or len(temp[iisbn])!=13:
        tmp[iisbn]='nan'
    if iisbn%10000==0:
        print(iisbn)
data.loc[:,'ISBN']=tmp
data.to_csv('item_info_books.csv',encoding="utf-8-sig")


f=open('isbn_scraped.pckl','wb')
isbn_list=set(data['ISBN'])
pickle.dump(isbn_list,f)
f.close()


#%%
import pickle
import pandas as pd
f=open('bookcomment.pckl','rb')
[iisbn,isbn_list,count,bookcomment]=pickle.load(f)
book_db=pd.DataFrame(bookcomment).to_csv('book_db.csv',encoding='utf-8-sig')