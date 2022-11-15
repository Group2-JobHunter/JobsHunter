from WebScraper import * 
import time
import pyshorteners as s
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

class LinkedIn(WebScraper):

    def __init__(self, path , jobTitle, location , skills):
        super().__init__(path,True)

        self.page = ""
        self.extractedJobs = []
        self.filteredJobs = []
        self.parsedJobs = []
         
        location  = location.replace(" " , '%20')
        jobTitle  = jobTitle.replace(" " , '%20')
        self.url = f"https://www.linkedin.com/jobs/search?keywords={jobTitle}&location={location}"

        self.skills = skills
    

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
                skills = len(self.skills)
                result = self.filter(str(jobDesc))

                if (result == 0):
                    continue
                result = f"Matched {int((result/skills)*100)} %"

                title = job.find_element(By.CLASS_NAME, "base-search-card__title").text
                company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text 
                location = job.find_element(By.CLASS_NAME, "job-search-card__location").text  
                date =job.find_element(By.TAG_NAME, "time").text
                link = job.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute('href') 
                link = short_.tinyurl.short(link)

                print ()
                
                print (title)
                print (result)
                print (company)
                print (location)
                print (date)
                print (link)
                
                print ()

            except Exception as e:
                print(f"Error Found : {title} in {company} ")
                print(e)
                pass
        
         

    
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

    
    def exportToDB(self):
        """
        saves the filtered data into the Database
        """
        pass

     



x = LinkedIn("../chromedriver", 'software developer' , 'Jordan, Amman', ['Nodejs' , 'OOP' , 'CSS' , "HTML" , "Git" , "React" , "Mysql" , "Java" , "Python" , "API" , "REst", "Asp.Net", "C#"])

x.loadWebsite()
x.extractor()
 