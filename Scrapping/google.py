import time
import re
from selenium.webdriver.common.by import By
import pyshorteners as s
from .WebScraper import * 
from .database import *
import datetime


# from database import Database
# from WebScraper import WebScraper

class Google(WebScraper):

    def __init__(self,job_title,city,skills):
        super().__init__(True)
        self.job_title=job_title
        self.city=city
        self.skills=skills
        self.filteredJobs=[]
      



    def start(self):
        print('google started')
        self.loadWebsite()
        self.extractor()
        print('google finished')




    def loadWebsite(self):
        job_name=re.sub(r'\s+', '+', self.job_title)
        skills='+'.join(self.skills)
        url=f'https://www.google.com/search?q={job_name}+{self.city}+{skills}&sxsrf=ALiCzsZIFgfwQJGi-qZoG7lhKz50z4Qf_A:1668968226798&ei=Im96Y-KCMNSJkdUPxY2TkAg&oq=jobs&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMgQIIxAnMgQIIxAnMgcIABDJAxBDMgUIABCRAjIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCC4QsQMQQzoKCC4QsQMQgwEQQzoECC4QQzoHCC4Q1AIQQzoICAAQgAQQsQM6BQgAEIAEOgsILhCABBCxAxCDAToOCC4QgAQQsQMQgwEQ1AI6CAguELEDEIMBOhYILhCDARCvARDHARDUAhCxAxCABBBDOgoIABCABBCHAhAUSgQIQRgASgQIRhgAUABYnwxgmB9oAXAAeAGAAekEiAGcD5IBCTItMi4xLjAuMpgBAKABAcABAQ&sclient=gws-wiz-serp&ibp=htl;jobs&sa=X&ved=2ahUKEwj7pPaWr737AhW9QUEAHSwTBTgQutcGKAF6BAgIEAY#fpstate=tldetail&htivrt=jobs&htidocid=gF9sc0GquhcAAAAAAAAAAA%3D%3D'
        time.sleep(2)
        
        self.driver.get(url)
        

    def timeToDate(self,string : str):
        
        try:
            string = string.replace('+',"")
            string = string.replace('-',"")
            # string = string.replace('hour',"hours")
            # string = string.replace('minute',"minutes")
            # string = string.replace('day',"days")
            # string = string.replace('week',"weeks")
            string = string.replace('Yesterday','1 days ago')
            string = string.replace('/',"")
            s = string
            
            parsed_s = [s.split()[:2]]
            time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
            dt = datetime.timedelta(**time_dict)
            past_time = datetime.datetime.now() - dt
            job_date = str(past_time).split(" ")[0]
            # print(job_date)
            return job_date 
        except:
            return string


    def extractor(self):
        """
        it uses the page property to extract the relevant jobOffers properties and writes into the self.extractedJobs
        which is a list dictionaries -> {jobPoster: "name of job poster",  FullJobDescribtion: "the describtion"}
        """
        listed_jobs=self.driver.find_elements(By.XPATH,'//div[@class="PwjeAc"]')
        time.sleep(1)
        for idx,i in enumerate(listed_jobs):

            self.scroll_into_job(i)
            i.click()
            time.sleep(2)
            
            # if self.driver.find_element(By.CSS_SELECTOR,'.WbZuDe'):

            #     print(self.driver.find_element(By.CSS_SELECTOR,'.WbZuDe').text)
            #     print('clicked')
            #     time.sleep(1)




            self.filteredJobs.append(self.get_job_information(i))


        self.driver.close()
        self.exportToDB(self.filteredJobs)


    def scroll_into_job(self,element):

        self.driver.execute_script('arguments[0].scrollIntoView(true);',element)   

    def get_job_information(self,job_card):
            job_title=job_card.find_element(By.CSS_SELECTOR,'.BjJfJf')
            company=job_card.find_element(By.CSS_SELECTOR,'.vNEEBe')
            location=job_card.find_element(By.CSS_SELECTOR,'.Qk80Jf')
            source=job_card.find_element(By.CSS_SELECTOR,'.Qk80Jf ~ .Qk80Jf')
            source_list=source.text.split(' ')
            
            date=job_card.find_element(By.CSS_SELECTOR,'.KKh3md .LL4CDc')
            formated_date=self.timeToDate(date.text)
            if not any(char.isdigit() for char in formated_date):
                formated_date=datetime.datetime.today().strftime('%Y-%m-%d')

            link=job_card.find_element(By.CSS_SELECTOR,'.pMhGee')
            description=self.driver.find_element(By.CSS_SELECTOR,'#tl_ditc')
            match_perc=int(self.match_percatnage(description.text))
            if match_perc==0:
                match_perc=70

            
     
            print(source_list[1],job_title.text,company.text,formated_date,location.text,'Jordan',match_perc,link.get_attribute("href"))
            


            return (source_list[1],job_title.text,company.text,formated_date,location.text,'Jordan',int(match_perc),link.get_attribute("href"))
            
        

    def match_percatnage(self,job_description):
        flag=0
        if len(self.skills)>0:

            for skill in self.skills:
                if skill.lower() in job_description.lower():
                    flag += 1

            if len(self.skills)>0:
                            percatnage=(str(int((flag / len(self.skills)) * 100)))

            else:
                            percatnage=('N/A')

        return percatnage


  
    def filter(self):
        """
        it uses self.extractedJobs and then filters(as in removing the tags and extracting the string inside them) the
        values in there, after that these values are added into self.filteredJobs which is a list dictionaries
        """
        pass

 
    def parser(self):
        """
        it uses self.filteredJobs and then creates the JobOffer object and fills it up
        """
        pass

  
    def exportToDB(self,data):
        """
        saves the filtered data into the Database
        """
        new_data=Database()
        new_data.save_data(data)



    
# bytt=Google('software developer','amman',['css','html'])

# bytt.start()

# print(bytt.filteredJobs)