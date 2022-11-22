import time
from database import *
from bs4 import BeautifulSoup
from WebScraper import *
from lxml import etree
import urllib.parse
import requests
import json


def list_to_string(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def get_description(job_url):
    print(job_url)
    result = requests.get(job_url)
    doc = BeautifulSoup(result.content, "html.parser")
    dom = etree.HTML(str(doc))
    # print(doc.prettify())
    posting_date = dom.xpath("/html/body/div/div[1]/div[4]/div[1]/p[2]")[0].text.removeprefix("Posted on: ").strip()
    # print(date)
    description = list_to_string(dom.xpath(f"/html/body/div/div[2]/div[1]/div[2]/div/p/text()")[0:30])
    requirements = list_to_string(dom.xpath(f"/html/body/div/div[2]/div[2]/div/div/p/text()")[0:30])
    full_description = description + requirements
    # print(full_description)
    time.sleep(1.5)
    return {"date": posting_date, "description": full_description, "url": job_url}


class GulfTalent(WebScraper):
    def __init__(self, job_title, country, city, skills=None):
        super().__init__(True)
        self.city_codes = {'Dubai': 10111111000111, 'Riyadh': 10111112000121, 'Abu Dhabi': 10111111000112,
                           'Doha': 10111114000151, 'Jeddah': 10111112000122, 'Sharjah': 10111111000113,
                           'Amman': 10229117000171, 'Cairo': 10229362000231, 'Al Ain': 10111111000115,
                           'Kuwait City': 10111113000131, 'Ras Al Khaimah': 10111111000117, 'Mecca': 10111112000127,
                           'Khobar': 10111112000124, 'Muscat': 10111116000162, 'Manama': 10111115000141,
                           'Ajman': 10111111000114, 'Basra': 10229120000214, 'Yanbu': 10111112000126,
                           'Beirut': 10229411000221, 'Fujairah': 10111111000116, 'Umm Al Quwain': 10111111000118,
                           'Jubail': 10111112000125, 'Erbil': 10229120000215, 'Dammam': 10111112000123,
                           'Tripoli': 10229118000181, 'Salalah': 10111116000161, 'Sulaymaniyah': 10229120000216,
                           'Dhahran': 10111112000128}
        self.country_codes = {'UAE': 10111111000000, 'Saudi Arabia': 10111112000000, 'Qatar': 10111114000000,
                              'Jordan': 10229117000000, 'Egypt': 10229362000000, 'Kuwait': 10111113000000,
                              'India': 90449397000000, 'Bahrain': 10111115000000, 'Oman': 10111116000000,
                              'Malta': 90999423000000, 'Iraq': 10229120000000, 'Lebanon': 10229411000000,
                              'United Kingdom': 90339515000000, 'Vietnam': 90449522000000, 'Pakistan': 90449455000000,
                              'Uganda': 90999513000000, 'Netherlands': 90999443000000, 'Australia': 90339311000000,
                              'Canada': 90339337000000, 'Maldives': 90449421000000, 'Algeria': 90229302000000,
                              'Libya': 10229118000000, 'New Zealand': 90339447000000, 'Greece': 90999381000000,
                              'Ghana': 90999379000000, 'Turkey': 90999509000000, 'France': 90999372000000,
                              'Ethiopia': 90999366000000, 'Germany': 90999378000000, 'Brunei': 90449330000000,
                              'Kenya': 90999406000000, 'Poland': 90999464000000, 'Swaziland': 90999496000000,
                              'Bangladesh': 90449315000000, 'Guinea': 90999387000000, 'Ivory Coast': 90999351000000,
                              'Denmark': 90999356000000, 'Morocco': 90229437000000, 'Israel': 90999401000000,
                              'Ireland': 90999400000000, 'Cyprus': 90999354000000, 'Sudan': 90229493000000,
                              'Palestine': 90229457000000, 'Portugal': 90999465000000, 'Luxembourg': 90999416000000,
                              'Hong Kong': 90449394000000, 'Djibouti': 90229357000000, 'Tanzania': 90999501000000,
                              'Norway': 90999454000000}
        self.job_title = urllib.parse.quote(job_title)
        self.city = urllib.parse.quote(city)
        self.country = country
        self.skills = skills
        self.applyURL = {}
        self.response_api = json.loads(requests.get(
            f"https://www.gulftalent.com/api/jobs/search?condensed=false&config%5Bfilters%5D=ENABLED&config%5Bresults"
            f"%5D=FILTERED&filters%5Bcountry%5D%5B0%5D="
            f"{self.get_country_code()}&include_scraped=1&limit=10000&search_keyword={self.job_title}&version=2").text)

    def start(self):
        print('started scraping from Gulf Talent')
        self.extractor()
        self.exportToDB()
        print('done scraping from Gulf Talent')

    def get_country_code(self):
        for key in self.country_codes.keys():
            if str(key).title() == self.country.title():
                print("country code: " + str(self.country_codes[key]))
                return self.country_codes[key]
        return ""

    def check_city(self):
        for key in self.city_codes.keys():
            if str(key).title() == self.city.title():
                print("city code: " + str(self.city_codes[key]))
                return list(self.city_codes.keys())[list(self.city_codes.values()).index(self.city_codes[key])]
        return "-"

    def get_country_codes_from_api(self):
        r = range(len(self.response_api["filters"]["country"]["items"]))
        for i in r:
            self.country_codes.update({self.response_api["filters"]["country"]["items"][i]["label"]["long"]: int(
                self.response_api["filters"]["country"]["items"][i]["id"])})
        print(self.country_codes)

    def get_city_codes_from_api(self):
        r = range(len(self.response_api["filters"]["city"]["items"]))
        for i in r:
            self.city_codes.update({self.response_api["filters"]["city"]["items"][i]["label"]["long"]: int(
                self.response_api["filters"]["city"]["items"][i]["id"])})
        print(self.city_codes)

    def get_match_rate(self, description):
        counter = 0
        # print(description)
        if self.skills:
            for skill in self.skills:
                # if description.lower().find(skill.lower()):
                if str(skill).lower() in description.lower():
                    counter = counter + 1
        else:
            return 0
        print("match rate in terms of skill: " + str((counter / len(self.skills) * 100)) + "%")
        return int(counter / len(self.skills) * 100)

    def loadWebsite(self, url):
        """
        takes the URL for the website and returns the page elements
        """
        for job in self.response_api["results"]["data"]:
            self.applyURL.update({"job_title": job["title"], "job_url": "http://gulfTalent.com" + job["link"]})
        # print(self.applyURL)

    def extractor(self):
        """
        it uses the page property to extract the relevant jobOffers properties and writes into the self.extractedJobs
        which is a list dictionaries -> {jobPoster: "name of job poster",  FullJobDescription: "the description"}
        """
        self.loadWebsite("not url")
        for job in self.response_api["results"]["data"]:
            self.extractedJobs.update({"jobPoster": job["company_name"], "FullJobDescription": get_description(
                "http://gulfTalent.com" + job["link"])})
            job = (
                "Gulf Talent", job["title"], job["company_name"], self.extractedJobs.get("FullJobDescription")["date"],
                self.check_city(),
                self.country, self.get_match_rate(self.extractedJobs.get("FullJobDescription")["description"]),
                self.extractedJobs.get("FullJobDescription")["url"])
            self.filteredJobs.append(job)
            print(job)

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
        # response = self.response_api["results"]["data"]
        # job = ("gulfTalent", response["title"], response["company_name"], self., city, country, percentage, link)
        pass

    def exportToDB(self):
        """
        saves the filtered data into the Database
        """
        db = Database()
        db.save_data(self.filteredJobs)

