import time
import re
from selenium.webdriver.common.by import By
import pyshorteners as s
from .WebScraper import * 
from .database import *

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
        print('start scrapping')
        self.loadWebsite()
        self.extractor()
        print('finish scrapping')

            
       
    def loadWebsite(self):

        job_name = re.sub(r'\s+', '-', self.jb_title)
        url = f'https://www.bayt.com/en/{self.country}/jobs/{job_name}-jobs/?options%5Bsort%5D%5B%5D=d'
        self.driver.get(url)




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

                        

                        job = ("Bayt",title.text,company.text,date.text,city, country,percatnage,link)
                        print(job)
                        self.filteredJobs.append(job)

                        

                        
                    
                        self.scroll += 20

                    else:

                        break


                except:
                    self.scroll += 20
                    continue
                break

        self.driver.close()
        self.exportToDB(self.filteredJobs)

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


