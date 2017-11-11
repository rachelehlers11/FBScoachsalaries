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

# First function scrapes the first table from the page.
# The ifelse statements in the makedataframe function are 
# specific to these web pages as well as the NaN replacements.


def makedataframe(link): 
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find_all('table')
    data = pd.read_html(str(table),encoding='utf-8')
    # ifelse to handle the waybackmachine's different table output
    if len(data) > 1:
        data = data[0].join(data[1], how = 'outer', on = None )
    else:
        data = data[0]
    data = data.replace('--', np.NaN) # null values in the table are '--'
    return data



#make the dataframes

# The extra removal of the last line, "[:-1]" , is required on 2016, 2017 dataframes to 
# remove the table headers at the bottom of the table whose purpose is visual astistance 

#head coaches
headcoachlink = 'http://sports.usatoday.com/ncaa/salaries/'
fourteen = makedataframe('https://web.archive.org/web/20141230041628/' + headcoachlink)
fifteen = makedataframe('https://web.archive.org/web/20151214221657/' + headcoachlink)
sixteen = makedataframe('https://web.archive.org/web/20161215053646/' + headcoachlink)
seventeen = makedataframe(headcoachlink)[:-1] # Remove extra table header at the bottom.

#assistant coaches
assistantlink = 'http://sports.usatoday.com/ncaa/salaries/football/assistant'
astfourteen = makedataframe('https://web.archive.org/web/20150129211154/' + assistantlink)
astfifteen = makedataframe('https://web.archive.org/web/20160130233153/' + assistantlink)
astsixteen = makedataframe(assistantlink)[:-1] # Remove extra table header at the bottom.

#strengthcoaches
strengthcoachlink = 'http://sports.usatoday.com/ncaa/salaries/football/strength'
strengthsixteen = makedataframe(strengthcoachlink)[:-1] # Remove extra table header at the bottom.




# Change column names for uniformity. Different lengths and different names,
# so had to be done manually 

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
astfourteen.columns = ['rank', 'school', 'conf', 'astcoach', 'schoolpay',\
                       'otherpay', 'totalpay', 'maxbonus', 'stafftotal']

astfifteen.columns = ['rank', 'school', 'conf', 'astcoach', 'schoolpay',\
                      'otherpay', 'totalpay', 'maxbonus', 'stafftotal']

astsixteen.columns = ['rank', 'school', 'conf', 'astcoach', 'schoolpay',\
                      'totalpay', 'maxbonus', 'stafftotal','buyout']

strengthsixteen.columns = ['rank', 'school', 'conf', 'astcoach', 'schoolpay',\
                           'totalpay', 'maxbonus' ,'stafftotal', 'buyout'] 


#list of dataframes for reference in loops
dflist = [fourteen, fifteen, sixteen, seventeen, astfourteen, astfifteen, \
          astsixteen, strengthsixteen]


# Now, want to make the money data useful by removing the symbols. While
# looping through each, item, might as well add another variable "category", which
# tells whether the school is a Power Five or not. Made a string so I wouldn't have
# to change plot labels in ggplot 


numericcolumns = ['rank', 'schoolpay', 'otherpay', 'totalpay', 'maxbonus', \
                  'bonusespaid', 'stafftotal']
powerfive = ['ACC', 'SEC', 'Big Ten', 'Big 12', 'PAC-12', 'Pac-12']


for item in dflist:
    for x in item.columns:
        item[x] = item[x].astype(str).str.replace('$', '')
        item[x] = item[x].astype(str).str.replace(',', '')
    item['category'] = ['Power Five' if x in powerfive else 'Others' for x in item['conf']]

#change the columns calculations will be made on to numeric.
    
for item in dflist:    
    for x in item.columns: 
        if x in numericcolumns:
            item[x] = pd.to_numeric(item[x], errors = 'coerce')



# Option: export to CSV. If any changes are made re-write them

os.chdir('/Users/rachelehlers/Desktop/DataBlogIdeas/sportsalary/FBSsalaries/salaryfiles')
f = '/Users/rachelehlers/Desktop/DataBlogIdeas/sportsalary/FBSsalaries/salaryfiles'
file = open('fourteen.txt', 'w', encoding = 'utf-8')
file.write(fourteen.to_csv(path = f, index = False))
file.close()

file = open('fifteen.txt', 'w', encoding = 'utf-8')
file.write(fifteen.to_csv(path = f, index = False))
file.close()


file = open('sixteen.txt', 'w', encoding = 'utf-8')
file.write(sixteen.to_csv(path = f, index = False))
file.close()

file = open('seventeen.txt', 'w', encoding = 'utf-8')
file.write(seventeen.to_csv(path = f, index = False))
file.close()

file = open('astfourteen.txt', 'w', encoding = 'utf-8')
file.write(astfourteen.to_csv(path = f, index = False))
file.close()

file = open('astfifteen.txt', 'w', encoding = 'utf-8')
file.write(astfifteen.to_csv(path = f, index = False))
file.close()

file = open('astsixteen.txt', 'w', encoding = 'utf-8')
file.write(astsixteen.to_csv(path = f, index = False))
file.close()

file = open('strengthsixteen.txt', 'w', encoding = 'utf-8')
file.write(strengthsixteen.to_csv(path = f, index = False))
file.close()






















        
        
        
        
        
        
        
        
