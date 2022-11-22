import time
import re
from selenium.webdriver.common.by import By
import pyshorteners as s
from .WebScraper import * 
from .database import *
import datetime


# from database import Database
# from WebScraper import WebScraper


class Bayt(WebScraper):

    def __init__(self, job_title,country,skill):
        super().__init__(True)
        self.scroll = 30
        self.jb_title=job_title
        self.country=country
        self.skill = skill
        self.filteredJobs=[]
        
        
        
    def start(self):
        print('BAYT STARTED')
        self.loadWebsite()
        self.extractor()
        print('BAYT FINISHED')
        self.driver.close()
        self.exportToDB(self.filteredJobs)

            
       
    def loadWebsite(self):

        job_name = re.sub(r'\s+', '-', self.jb_title)
        url = f'https://www.bayt.com/en/{self.country}/jobs/{job_name}-jobs/?options%5Bsort%5D%5B%5D=d'
        self.driver.get(url)


    def timeToDate(self,string : str):
        
        try:
            string = string.replace('+',"")
            string = string.replace('-',"")
            string = string.replace('hour',"hours")
            string = string.replace('minute',"minutes")
            string = string.replace('day',"days")
            string = string.replace('week',"weeks")
            string = string.replace('1 month ago',"1 months ago")
            string = string.replace('ss',"s")
            string = string.replace('Just now','0 days ago')
            string = string.replace('Yesterday','1 days ago')
            string = string.replace('/',"")
            s = string
            
            parsed_s = [s.split()[:2]]
            time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
            dt = datetime.timedelta(**time_dict)
            past_time = datetime.datetime.now() - dt
            job_date = str(past_time).split(" ")[0]
             
            return job_date 
        except:
            return string

    def extractor(self):
        """
        it uses the page property to extract the relevant jobOffers properties and writes into the self.extractedJobs
        which is a list dictionaries -> {jobPoster: "name of job poster",  FullJobDescribtion: "the describtion"}
        """


        job_link = self.driver.find_elements(by=By.CSS_SELECTOR, value='.has-pointer-d')
        self.driver.maximize_window()

        for i in job_link:
            while True:
                try:

                    title = i.find_element(by=By.CSS_SELECTOR, value='.jb-title')
                    title.click()
                    time.sleep(2)
                    job_description = self.driver.find_elements(by=By.CSS_SELECTOR, value='.card-content')

                    flag = 0
                    skills_length = len(self.skill)
                    for skill in self.skill:
                        if skill.lower() in job_description[1].text.lower():
                            flag += 1
                            

                    if flag >= 1 or len(self.skill)==0:

                        company = i.find_element(by=By.CSS_SELECTOR, value='.jb-company')
                     
                        location = i.find_element(by=By.CSS_SELECTOR, value='.jb-loc')
                        
                        date = i.find_element(by=By.CSS_SELECTOR, value='.jb-date')
                        
                        link = self.driver.current_url
                        

                        
                        

                        self.driver.execute_script(f"window.scrollBy(0,{self.scroll})", "")
                        
                        if len(self.skill)>0:
                            percatnage=(str(int((flag / skills_length) * 100)))

                        else:
                            percatnage=('N/A')
                        city , country = location.text.split(',')[0] , location.text.split(',')[1]

                        
                        date = self.timeToDate(date.text)
                        job = ("Bayt",title.text,company.text,date,city, country,percatnage,link)
                         
                        self.filteredJobs.append(job)

                        

                        
                    
                        self.scroll += 20

                    else:

                        break


                except:
                    self.scroll += 20
                    continue
                break



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
       









# bytt=Bayt('web developer','jordan',[])

# bytt.start()

# # new_data=Database()
# # print(new_data.fetch_data())


