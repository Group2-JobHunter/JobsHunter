from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class WebScraper(ABC):
    def __init__(self,headless):
        options = Options()
        user_agent = (
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        )
        options.headless = headless
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
        options.add_argument("--lang=en-GB")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        

        self.page = ""
        self.extractedJobs = []
        self.filteredJobs = []
        self.parsedJobs = []

    @abstractmethod
    def loadWebsite(self, URL):
        """
        takes the URL for the website and returns the page elements
        """
        pass

    @abstractmethod
    def extractor(self):
        """
        it uses the page property to extract the relevant jobOffers properties and writes into the self.extractedJobs
        which is a list dictionaries -> {jobPoster: "name of job poster",  FullJobDescribtion: "the describtion"}
        """
        pass

    @abstractmethod
    def filter(self):
        """
        it uses self.extractedJobs and then filters(as in removing the tags and extracting the string inside them) the
        values in there, after that these values are added into self.filteredJobs which is a list dictionaries
        """
        pass

    @abstractmethod
    def parser(self):
        """
        it uses self.filteredJobs and then creates the JobOffer object and fills it up
        """
        pass

    @abstractmethod
    def exportToDB(self):
        """
        saves the filtered data into the Database
        """
        pass
