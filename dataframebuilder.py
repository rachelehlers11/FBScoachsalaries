#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 17:26:37 2017

@author: rachelehlers
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def makedataframe(link): 
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find_all('table')
    name = pd.read_html(str(table),encoding='utf-8')
    if len(name) > 1:
        name = name[0].join(name[1], how = 'outer', on = None )
    else:
        name = name[0]
    name = name.replace('--', np.NaN)
    return name
#make the dataframes
#the extra index is required on 2016, 2017 dataframes to remove the table headers at the bottom of the table whose purpose is visual assistance 

#head coaches
hclink = 'http://sports.usatoday.com/ncaa/salaries/'
fourteen = makedataframe('https://web.archive.org/web/20141230041628/' + hclink)
fifteen = makedataframe('https://web.archive.org/web/20151214221657/' + hclink)
sixteen = makedataframe('https://web.archive.org/web/20161215053646/' + hclink)
seventeen = makedataframe(hclink)[:-1]

#assistant coaches
aclink = 'http://sports.usatoday.com/ncaa/salaries/football/assistant'
assfourteen = makedataframe('https://web.archive.org/web/20150129211154/' + aclink)
assfifteen = makedataframe('https://web.archive.org/web/20160130233153/' + aclink)
asssixteen = makedataframe(aclink)[:-1]

#strengthcoaches
strengthsixteen = makedataframe('http://sports.usatoday.com/ncaa/salaries/football/strength')[:-1]




# now look at the column names, either on the site or by calling df.columns. 
# change for uniformity/simplicity
fourteen.columns = ['rank', 'school', 'conf', 'headcoach', 'schoolpay',\
                    'otherpay', 'totalpay', 'maxbonus', 'stafftotal']

fifteen.columns = ['rank', 'school', 'conf', 'headcoach', 'schoolpay',\
                   'otherpay', 'totalpay', 'maxbonus', 'bonusespaid', \
                   'stafftotal']

sixteen.columns = ['rank', 'school', 'conf', 'headcoach', 'schoolpay',\
                   'otherpay', 'totalpay', 'maxbonus', 'bonusespaid',\
                   'stafftotal']

seventeen.columns = ['rank', 'school', 'conf', 'headcoach', 'schoolpay',\
                     'totalpay', 'maxbonus', 'bonusespaid', 'stafftotal', \
                     'buyout']
assfourteen.columns = ['rank', 'school', 'conf', 'asscoach', 'schoolpay',\
                       'otherpay', 'totalpay', 'maxbonus', 'stafftotal']

assfifteen.columns = ['rank', 'school', 'conf', 'asscoach', 'schoolpay',\
                      'otherpay', 'totalpay', 'maxbonus', 'stafftotal']

asssixteen.columns = ['rank', 'school', 'conf', 'asscoach', 'schoolpay',\
                      'totalpay', 'maxbonus', 'stafftotal','buyout']

strengthsixteen.columns = ['rank', 'school', 'conf', 'asscoach', 'schoolpay',\
                           'totalpay', 'maxbonus' ,'stafftotal', 'buyout'] 


#list of dataframes for reference in loops
dflist = [fourteen, fifteen, sixteen, seventeen, assfourteen, assfifteen, \
          asssixteen, strengthsixteen]


# clean the data 
numericcolumns = ['rank', 'schoolpay', 'otherpay', 'totalpay', 'maxbonus', \
                  'bonusespaid', 'stafftotal']
powerfive = ['ACC', 'SEC', 'Big Ten', 'Big 12', 'Pac-12']
for item in dflist:
    for x in item.columns:
        item[x] = item[x].astype(str).str.replace('$', '')
        item[x] = item[x].astype(str).str.replace(',', '')
    item['category'] = ['Power Five' if x in powerfive else 'Others' for x in item['conf']]
    
for item in dflist:    
    for x in item.columns: 
        if x in numericcolumns:
            item[x] = pd.to_numeric(item[x], errors = 'coerce')
































        
        
        
        
        
        
        
        