#!/usr/local/bin/env python
##########################################################################

#Script for extracting today's values from Bloomberg Billionaires Index 
# https://www.bloomberg.com/billionaires/

###########################################################################

from lxml import html
import requests

#Getting the webpage and building tree
page = requests.get('https://www.bloomberg.com/billionaires/')
tree = html.fromstring(page.content)


#This will create a list of ranks 
rank = tree.xpath('//div[@class="table-cell t-rank"]/text()')

#This will create a list of names 
name = tree.xpath('//div[@class="table-cell t-name"]/a')
name_res = [x.text if x.text else '' for x in name]

#This will create a list of total net worth
activetnw = tree.xpath('//div[@class="table-cell active t-nw"]')
activetnw_res = [x.text if x.text else '' for x in activetnw]
del activetnw_res[0]

#This will create a list of last changes
lastchange = tree.xpath('//div[@class="table-cell t-lcd pos"]/text()| //div[@class="table-cell t-lcd neg"]/text() | //div[@class="table-cell t-lcd none"]/text()')
#lastchange_res = [x.text if x.text else '' for x in lastchange]

#This will create a list of YTD changes
ytdchange = tree.xpath('//div[@class="table-cell t-ycd pos"]/text() | //div[@class="table-cell t-ycd neg"]/text()| //div[@class="table-cell t-ycd none"]/text()')


#This will create a list of countries
country = tree.xpath('//div[@class="table-cell t-country"]')
country_res = [x.text if x.text else '' for x in country]
del country_res[0]

#This will create a list of industries
industry = tree.xpath('//div[@class="table-cell t-industry"]')
industry_res = [x.text if x.text else '' for x in industry]
del industry_res[0]


# To print the lists:
#print ('rank: ', rank)
#print ('name: ', name_res)
#print ('activetnw: ', activetnw)
#print('lastchange:', lastchange)
#print ('ytdchange: ', ytdchange)
#print ('country: ', country_res)
#print ('industry: ', industry_res)

#Saving the data as csv
import pandas
import datetime
#check the length of the lists
print(len(rank), len(name_res), len(activetnw_res), len(lastchange), len(ytdchange), len(country_res), len(industry_res)) 

#creates a pandas df out of the lists
df = pandas.DataFrame(data={"rank": rank, "name": name_res, "activetnw": activetnw_res, 
"lastchange": lastchange, "ytdchange": ytdchange, "country": country_res, "industry": industry_res})

#write a DF to csv with current date name
now = datetime.datetime.now()
snapshotdate = str(now)[:10]
df.to_csv(open(snapshotdate+'.csv','w'),index=False)