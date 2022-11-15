import sqlite3
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By

from bayt import Bayt

bytt=Bayt(r'C:\Users\ibrah\Downloads\chromedriver_win32 (1)\chromedriver',False,['react','html'])
bytt.loadWebsite('jordan','web developer')
bytt.extractor()
bytt.parser()
data=bytt.extracted_jobs
print(data)
db=sqlite3.connect('app.db')

cr=db.cursor()

cr.execute('create table if not exists Jobs (Title text,Location text, Date text, Company text,Source text,Link text,Match text )')

#inserting data bayt

for n in range(len(data['jobtitle'][0])):

    job=data['jobtitle'][0][n]
    location=data['location'][0][n]
    date= data['date'][0][n]
    company= data['company'][0][n]
    link=data['link'][0][n]
    # discription=data['descr'][n][0]
    match=data['match'][0][n]
    source=data['source'][0][n]
    cr.execute(f"INSERT INTO Jobs VALUES ('{job}', '{location}', '{date}','{company}','{source}','{link}','{match}')")
  
    

db.commit()


db.close()        


