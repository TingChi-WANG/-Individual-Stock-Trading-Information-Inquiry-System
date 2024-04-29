#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests,json,time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stock=input('請輸入個股代碼')  
struct_time = time.localtime(time.time())
ntime=time.strftime("%Y%m%d",struct_time)

driver = webdriver.Firefox()
driver.get('https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html')
search_box = driver.find_element('name','stockNo')
search_box.send_keys(stock)
search_box.send_keys(Keys.CONTROL, '\ue007')

url=f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={ntime}&stockNo={stock}'
data=requests.get(url)
datadict=json.loads(data.text)
cols=[]
for c in range(9):
    col0=[]
    for r in range(0,len(datadict['data'])):
        if c>=3 and c<=6:
            col0.append(float(datadict['data'][r][c]))
        elif c==7:
            datadict['data'][r][c]=datadict['data'][r][c].replace('X','')
            datadict['data'][r][c]=str(datadict['data'][r][c]).replace('+','')
            col0.append(float(datadict['data'][r][c]))
        else:
            col0.append(datadict['data'][r][c])
    cols.append((col0))
dic={}
head=datadict['fields']
for f in range(0,len(datadict['fields'])):
    dic[head[f]]=cols[f]
df=pd.DataFrame(dic)

plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
plt.plot(df['日期'],df['收盤價'])
plt.xlabel('日期')
plt.ylabel('收盤價')
plt.title('收盤價趨勢圖')

title=datadict['title']
def color_neg_pos(val):
    if val > 0:
        return 'color:red'
    elif val<0:
        return 'color:green'

(df.style.set_caption(title)
        .background_gradient('Blues', subset='收盤價')
        .format('{:.2f}', subset='漲跌價差')
        .applymap(color_neg_pos,subset='漲跌價差')
        )


# In[ ]:




