# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 10:30:06 2016

@author: Kelly
"""

import os
import pandas as pd


#import perscription data

os.chdir(r'C:\Users\Kelly\Desktop\Work\Opioid Issues')
p = pd.read_csv('Medicare_Part_D_Opioid_Prescriber_Summary_File(1).csv', dtype={'NPPES Provider ZIP Code':str,'Opioid Claim Count':float }, encoding ='UTF8')

#reformating zip codes for merge
p['Zip'] = p['NPPES Provider ZIP Code'].str[:5]

pop  = pd.read_csv('2010_pop.csv', dtype={'Zip':str, 'Pop':float}, encoding ='UTF8')
p_pop = pd.merge(p,pop,how='inner')

#filtering for more than 10 claims
p_pop_c  = p_pop[p_pop['Opioid Claim Count']>10]
x = p_pop_c['Specialty Description'].value_counts()
y = list(x.index)

#removing student category as it is a catch all category.  
y.pop(7)

bad_actors = []
for i in y: 
    test = p_pop_c[p_pop_c['Specialty Description']==i]
    test['Opioid'] = test['Opioid Claim Count']/test['Total Claim Count']
    test['Opioid_perc_zscore'] = (test.Opioid - test.Opioid.mean())/test.Opioid.std()
    test_bad_actors= test[test['Opioid_perc_zscore']>3]
    bad_actors.append(test_bad_actors)
bad_actors = pd.concat(bad_actors)

chart = bad_actors['Specialty Description'].value_counts()
chart.plot(kind='bar')
bad_actors.to_csv('bad_actors.csv')