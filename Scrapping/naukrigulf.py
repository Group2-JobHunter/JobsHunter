from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .database import Database
import datetime


from selenium.webdriver.common.by import By
class Naukrigulf():
        def __init__(self,jobTitle,city, country,skills):

                options = Options()
                user_agent = (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                )
                options.headless = True
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
                job_details=jobTitle.replace(" ","-")
                self.city=city
                self.country=country
                self.url = f"https://www.naukrigulf.com/{job_details}-jobs-in-{city}-{country}?sort=date"
                self.skills = skills
                self.herf_list=[]
                self.filteredJobs=[]


        def monthToNum(self,shortMonth):
                return {
                        'jan': "01",
                        'feb': "02",
                        'mar': "03",
                        'apr': "04",
                        'may': "05",
                        'jun': "06",
                        'jul': "07",
                        'aug': "08",
                        'sep': "09", 
                        'oct': 10,
                        'nov': 11,
                        'dec': 12
                }[shortMonth]

        def stringToDate(self,string:str):
                try:
                        print(string)
                        date = ''
                        if "ago" in string:
                                date = self.timeToDate(string)
                        else:
                                string = string.replace('on ','')
                                string = string.split(' ')
                                day = string[0]
                                month = self.monthToNum(string[1].lower())
                                today = datetime.date.today()
                                year = today.year
                                if int(day) < 10:
                                        day = f"0{day}"
                                date = f"{year}-{month}-{day}"
                        print(date)
                        return date
                except Exception as e:
                        print(e)



        def timeToDate(self,string : str):

                try:
                        if 'Posted' in string:
                                string = '1 days ago'
                        string = string.replace('+',"")
                        string = string.replace('-',"")
                        string = string.replace('hour',"hours")
                        string = string.replace('minute',"minutes")
                        string = string.replace('day',"days")
                        string = string.replace('week',"weeks")
                        string = string.replace('1 month ago',"1 months ago")
                        string = string.replace('ss',"s")
                        string = string.replace('Yesterday','1 days ago')
                        string = string.replace('Just now','0 days ago')
                        string = string.replace('/',"")
                        s = string

                        parsed_s = [s.split()[:2]]
                        time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
                        dt = datetime.timedelta(**time_dict)
                        past_time = datetime.datetime.now() - dt
                        job_date = str(past_time).split(" ")[0]
                        #print(job_date)
                        return job_date 
                except:
                        return string

        def get_herf(self):
                self.driver
                self.driver.get(self.url)
                for i in range(27):
                        try:
                                for element in self.driver.find_elements(By.XPATH, f'//*[@id="searchResult"]/div/section[2]/div[2]/div[2]/div[{i}]/a[1]'):
                                        if i == 2:
                                                continue
                                        c = element.get_attribute("href")
                                        time.sleep(1.5)
                                        
                                        self.herf_list.append(c)

                        except:
                                print('error')
                

        

        def get_job_details(self):
                driver=self.driver
                try:
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
                                
                                date = self.stringToDate(date.text[7:])
                                if (result == 0):
                                        continue
                                percentage = int((result/len_skills)*100)
                                job = ('Naukrigulf', job_titel.text, company_name.text,date,city,country,percentage,url)
                                self.filteredJobs.append(job)

                                
                                # job= ('naukrigulf', job_titel.text, company_name.text,date.text[7:], job_location.text,job_description.text, experience.text,url)
                                # self.filteredJobs.append(job)
                                print(job)
                except Exception as e:
                        print(e)
                        
                #driver.quit()
                self.exportToDB(self.filteredJobs)

        def filter(self,job_description):
                count = 0
                job_description = job_description.lower()
                for skill in self.skills:
                        if skill.lower() in job_description:
                                count+=1
                return count

        def start(self):
                try:
                        print("NAUKRI STARTED")
                        self.get_herf()
                        self.get_job_details()
                        print("NAUKRI FINISHED")
                except:
                        print('ERROR IN NUKRI')
        
        def exportToDB(self,data):
                new_data=Database()
                new_data.save_data(data)

# if __name__ == "__main__":
#         naukrigulf = naukrigulf("full stack devloper","amman","jordan",["python","java","c++"])
#         naukrigulf.get_jobs()


