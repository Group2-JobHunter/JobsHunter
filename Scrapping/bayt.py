import time
import re
import os


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyshorteners as s



from .WebScraper import WebScraper

class Bayt (WebScraper):

    def __init__(self, jobTitle, country , skills = [] ):
        super().__init__(False)
        self.scroll=30
        self.extracted_jobs={'jobtitle': [],  'location': [],'date':[],'company':[],'source':[],'link':[],'descr':[],'match':[]}
        self.skill=skills
        self.job_title=[]
        self.company=[]
        self.location=[]
        self.date=[]
        self.job_link=[]
        self.job_discription=[]
        self.match_perc=[]
        self.source=[]

        self.country = country
        self.jobTitle = jobTitle

        self.filteredJobs = []


    def start(self):
        self.loadWebsite()
        self.extractor()
        self.parser()
        print("BAYT FINISHED ")

    def loadWebsite(self):
        
        job_name=re.sub(r'\s+', '-', self.jobTitle)
        url=f'https://www.bayt.com/en/{self.country}/jobs/{job_name}-jobs/'
        return self.driver.get(url)


    
    def extractor(self):
        """
        it uses the page property to extract the relevant jobOffers properties and writes into the self.extractedJobs
        which is a list dictionaries -> {jobPoster: "name of job poster",  FullJobDescribtion: "the describtion"}
        """
        short_ = s.Shortener() 
        job_link=self.driver.find_elements(by=By.CSS_SELECTOR, value='.has-pointer-d')
        self.driver.maximize_window()
        time.sleep(1)
        ul = self.driver.find_element(By.XPATH, '/html/body/div[4]/section[2]/div[1]/div/div[1]/div[2]/ul')
        jobs_lis = ul.find_elements(By.TAG_NAME, "li")
        print()
        print("NUMBER OF JOBS")
        print(len(jobs_lis))
        for idx,i in enumerate(jobs_lis):
            # while True:
            try:
                
                
                title = i.find_element(by=By.CSS_SELECTOR, value='.jb-title')
                company = i.find_element(by=By.CSS_SELECTOR, value='.jb-company')
                self.company.append(company.text)
                location = i.find_element(by=By.CSS_SELECTOR, value='.jb-loc')
                self.location.append(location.text)
                date = i.find_element(by=By.CSS_SELECTOR, value='.jb-date')
                self.date.append(date.text)
                link = self.driver.current_url
                self.job_link.append(link)
                time.sleep(1)
                print()
                print()
                print("BAYT" , title.text)
                print()
                print()
                
                title.click()
                time.sleep(0.5)

                job_description =self.driver.find_elements(by=By.CSS_SELECTOR, value='.card-content')
                
                desc =job_description[1].text.lower()
                print()
                print()
                print(desc)
                print()
                print()



                self.job_discription.append(desc)
                self.job_title.append(title.text)

                link = short_.tinyurl.short(link)

                self.driver.execute_script(f"window.scrollBy(0,{self.scroll})", "")
                #self.match_perc.append(f'matched {int((flag/skills_length)*100)}%')
                self.source.append('Bayt')

                print()
                print()
                print("BAYT" , title.text)
                print()
                print()

                if len(self.skill) == 0:
                    city , country = location.text.split(',')[0] , location.text.split(',')[1]
                    job = ("Bayt",title.text,company.text,date.text,city, country,"N/A",link)
                    self.match_perc.append("N/A")
                    self.filteredJobs.append(job)
                    

                else:
                    flag = self.filter(desc)
                    skills_length = len(self.skill)
                    if flag>=1 :
                        percent = int((flag/skills_length)*100)
                        city , country = location.text.split(',')[0] , location.text.split(',')[1]
                        job = ("Bayt",title.text,company.text,date.text,city, country,percent,link)
                        self.filteredJobs.append(job)
                        

                        # Save to DB
                time.sleep(0.5)
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight * 0.02);")
                    # break


            except Exception as e:
                
                print()
                print(e)
                print()
                continue
                

        self.driver.close()




    def filter(self,desc):
        flag = 0
        skills_length=len(self.skill)
        for skill in self.skill:
            if skill.lower() in desc :
                flag += 1
        return flag


        

    
    def parser(self):
        """
        it uses self.filteredJobs and then creates the JobOffer object and fills it up
        """
        
        self.extracted_jobs['jobtitle'].append(self.job_title)
        self.extracted_jobs['location'].append(self.location)
        self.extracted_jobs['link'].append(self.job_link)
        self.extracted_jobs['date'].append(self.date)
        self.extracted_jobs['company'].append(self.company)
        self.extracted_jobs['descr'].append(self.job_discription)
        self.extracted_jobs['match'].append(self.match_perc)
        self.extracted_jobs['source'].append(self.source)

        return self.extracted_jobs

    def exportToDB(self):
        """
        saves the filtered data into the Database
        """
        pass





# bytt=Bayt(r'C:\Users\ibrah\Downloads\chromedriver_win32 (1)\chromedriver',False,['react','html'])
# bytt.loadWebsite('jordan','web developer')
# bytt.extractor()
# bytt.parser()

# data=bytt.extracted_jobs
# print(data)