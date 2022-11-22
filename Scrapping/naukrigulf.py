from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from .database import *
from database import Database



from selenium.webdriver.common.by import By
class naukrigulf():
        def __init__(self,job_details,city, country,skills):

                options = Options()
                user_agent = (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                )
                options.headless = False
                options.add_experimental_option("detach", True)
                options.add_argument(f"user-agent={user_agent}")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--ignore-certificate-errors")
                options.add_argument("--allow-running-insecure-content")
                options.add_argument("--disable-extensions")
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")
                options.add_argument("--start-maximized")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                job_details=job_details.replace(" ","-")
                self.city=city
                self.country=country
                self.url = f"https://www.naukrigulf.com/{job_details}-jobs-in-{city}-{country}?sort=date"
                self.skills = skills
                self.herf_list=[]
                self.filteredJobs=[]



        def get_herf(self):
                self.driver
                self.driver.get(self.url)
                for i in range(27):
                        try:
                                for element in self.driver.find_elements(By.XPATH, f'//*[@id="searchResult"]/div/section[2]/div[2]/div[2]/div[{i}]/a[1]'):
                                        if i == 2:
                                                continue
                                        c = element.get_attribute("href")
                                        time.sleep(3)
                                        self.herf_list.append(c)

                        except:
                                print('error')
        

        def get_job_details(self):
                driver=self.driver
                for i in self.herf_list:
                        driver.get(i)
                        time.sleep(3)
                        company_name = driver.find_element(By.CSS_SELECTOR, '.info-org')
                        job_titel = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/section[1]/div[1]/div[1]/h1')
                        job_location = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/section[1]/div[3]/div[1]/div[1]/div[2]/p[2]')
                        city= job_location.text.split('-')[0] 
                        country=job_location.text.split('-')[1]
                        experience = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/section[1]/div[3]/div[1]/div[1]/div[1]/p[2]')
                        job_description = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/section[1]/div[3]/article/section/div')
                        date= driver.find_element(By.CLASS_NAME, 'jd-timeVal')
                        url = driver.current_url
                        len_skills = len(self.skills)
                        result=self.filter(job_description.text)
                        if (result == 0):
                                continue
                        percentage = int((result/len_skills)*100)
                        job = ('naukrigulf', job_titel.text, company_name.text,date.text[7:],city,country,percentage,url)
                        self.filteredJobs.append(job)

                        
                        # job= ('naukrigulf', job_titel.text, company_name.text,date.text[7:], job_location.text,job_description.text, experience.text,url)
                        # self.filteredJobs.append(job)
                        print(job)
                driver.quit()
                self.exportToDB(self.filteredJobs)

        def filter(self,job_description):
                count = 0
                job_description = job_description.lower()
                for skill in self.skills:
                        if skill.lower() in job_description:
                                count+=1
                return count

        def start(self):
                self.get_herf()
                self.get_job_details()
                return self.filteredJobs
        
        def exportToDB(self,data):
                new_data=Database()
                new_data.save_data(data)

if __name__ == "__main__":
        naukrigulf = naukrigulf("full stack devloper","amman","jordan",["python","java","c++"])
        naukrigulf.get_jobs()


