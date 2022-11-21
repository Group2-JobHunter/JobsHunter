from .WebScraper import * 
import time
import pyshorteners as s
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from database import *
import datetime

class LinkedIn(WebScraper):

    def __init__(self, jobTitle, city, country , skills):
        super().__init__(True)

        self.page = ""
        self.extractedJobs = []
        self.filteredJobs = []
        self.parsedJobs = []
        self.city = city
        self.country = country

        location = f"{country}, {city}"
        location  = location.replace(" " , '%20')
        jobTitle  = jobTitle.replace(" " , '%20')
        self.url = f"https://www.linkedin.com/jobs/search?keywords={jobTitle}&location={location}&f_TPR=r604800"

        self.skills = skills

        

        # self.DB = Database()



 
    def start(self):
        self.loadWebsite()
        self.extractor()
        print("LINKEDIN FINISHED")
        self.driver.close()
        self.exportToDB(self.filteredJobs)
    

    def timeToDate(self,string):
        
        try:
            string = string.replace('+',"")
            string = string.reaplce('-',"")
            string = string.reaplce('hour',"hours")
            string = string.reaplce('minute',"minutes")
            string = string.reaplce('day',"days")
            string = string.reaplce('week',"weeks")
            string = string.reaplce('/',"")
            s = string
            
            parsed_s = [s.split()[:2]]
            time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
            dt = datetime.timedelta(**time_dict)
            past_time = datetime.datetime.now() - dt
            job_date = str(past_time).split(" ")[0]
            print(job_date)
            return job_date 
        except:
            return string

    def scrollWebPage(self):
        
        count = 6
        driver = self.driver
        
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while count > 0:
            count -=1

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            
            if lastHeight == newHeight:
                driver.execute_script("window.scrollTo(200,300);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                break
            lastHeight = newHeight
    

    def loadWebsite(self):
        self.driver.get(self.url)
        #self.scrollWebPage()
        self.page = self.driver.page_source



    
    def extractor(self):
        time.sleep(1)

        short_ = s.Shortener()        
        jobs_lis = self.driver.find_elements(By.CLASS_NAME, "jobs-search__results-list")[0].find_elements(By.TAG_NAME, "li")
        
        for job in jobs_lis:
            try:
                job.click()
                time.sleep(1.45)
                driver = self.driver
                showmore = driver.find_element(By.XPATH, "/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/button[1]")
                showmore.click()
                time.sleep(1.45)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                jobDesc = soup.find('div' , class_ = "show-more-less-html__markup" )

                title = job.find_element(By.CLASS_NAME, "base-search-card__title").text
                company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text 
                location = job.find_element(By.CLASS_NAME, "job-search-card__location").text  
                date =job.find_element(By.TAG_NAME, "time").text
                date = self.timeToDate(str(date))
                link = job.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute('href') 
                link = short_.tinyurl.short(link)

                len_skills = len(self.skills)
                if len_skills == 0:
                    job = ("LinkedIn",title,company,date,self.city,self.country,"N/A",link)
                    self.filteredJobs.append(job)
                else:
                    result = self.filter(str(jobDesc))
                    if (result == 0):
                        continue
                    percent = int((result/len_skills)*100)
                    job = ("LinkedIn",title,company,date,self.city,self.country,percent,link)
                    self.filteredJobs.append(job)

                print()
                print()
                print("LINKEDIN", title)
                print()
                print()

            except Exception as e:
                print(f"Error Found ")

    def filter(self,jobDesc):
        count = 0
        jobDesc = jobDesc.lower()
        for skill in self.skills:
            if skill.lower() in jobDesc:
                count+=1
        return count

    
    def parser(self):

        short_ = s.Shortener()
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

     



#x=  LinkedIn("../chromedriver", 'software developer' , 'Jordan, Amman', ['Nodejs' , 'OOP' , 'CSS' , "HTML" , "Git" , "React" , "Mysql" , "Java" , "Python" , "API" , "REst", "Asp.Net", "C#"])

