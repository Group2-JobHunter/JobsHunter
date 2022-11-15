import time
import re
import os


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By



from WebScraper import WebScraper

class Bayt (WebScraper):

    def __init__(self, path,headless,skill:list):
        super().__init__(path,headless)
        self.scroll=30
        self.extracted_jobs={'jobtitle': [],  'location': [],'date':[],'company':[],'source':[],'link':[],'descr':[],'match':[]}
        self.skill=skill
        self.job_title=[]
        self.company=[]
        self.location=[]
        self.date=[]
        self.job_link=[]
        self.job_discription=[]
        self.match_perc=[]
        self.source=[]




    def loadWebsite(self,country,required_job):

        job_name=re.sub(r'\s+', '-', required_job)
        url=f'https://www.bayt.com/en/{country}/jobs/{job_name}-jobs/'
        return self.driver.get(url)
    
    
    def extractor(self):
        """
        it uses the page property to extract the relevant jobOffers properties and writes into the self.extractedJobs
        which is a list dictionaries -> {jobPoster: "name of job poster",  FullJobDescribtion: "the describtion"}
        """
        job_link=self.driver.find_elements(by=By.CSS_SELECTOR, value='.has-pointer-d')
        self.driver.maximize_window()
        
        for i in job_link:
            while True:
                try:


                    title = i.find_element(by=By.CSS_SELECTOR, value='.jb-title')
                    title.click()
                    time.sleep(2)
                    job_description =self.driver.find_elements(by=By.CSS_SELECTOR, value='.card-content')
                    
                    flag = 0
                    skills_length=len(self.skill)
                    for skill in self.skill:
                        if skill.lower() in job_description[1].text.lower():
                            flag += 1
                            break


                    if flag>=1 :
                            
                    
                            company = i.find_element(by=By.CSS_SELECTOR, value='.jb-company')
                            self.company.append(company.text)
                            location = i.find_element(by=By.CSS_SELECTOR, value='.jb-loc')
                            self.location.append(location.text)
                            date = i.find_element(by=By.CSS_SELECTOR, value='.jb-date')
                            self.date.append(date.text)
                            link = self.driver.current_url
                            self.job_link.append(link)
                                   
                            self.job_discription.append(job_description[1].text)
                            self.job_title.append(title.text)
                            
                            self.driver.execute_script(f"window.scrollBy(0,{self.scroll})", "")
                            self.match_perc.append(f'matched {int((flag/skills_length)*100)}%')
                            self.source.append('Bayt')
                            print('------------------------------------------')
                            print(self.job_title)
                            self.scroll += 20

                    else:

                            break


                except:
                    self.scroll += 30
                    continue
                break

        self.driver.close()


        

    
        
      


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