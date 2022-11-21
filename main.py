import eel
import time
from threading import Thread
 
from Scrapping.Linkedin import LinkedIn
from Scrapping.bayt import Bayt
from Scrapping.database import Database
from Scrapping.google import Google

results =[]

#f"LinkedIn,{title},{company},{date},{location},{link},{title}"

title = keywords = country = city = ""

@eel.expose
def setSearch_data(data):
    global title , keywords , country , city
    title = data['title']
    keywords = data['keywords']
    country = data['country']
    city = data['city']


@eel.expose
def start_scrapping():
        global results
        results = []
        global title , keywords , country , city

        print(title , keywords , country , city)

        linkedin = LinkedIn(title,city,country,keywords)
        bayt = Bayt(title,country,keywords)
        google=Google(title,city,keywords)


        print ("Scraping Started")

        t1 = Thread(target=linkedin.start, args=())
        t2 = Thread(target=bayt.start, args=())
        t3 = Thread(target=google.start, args=())
        # t1.start()
        t2.start()
        t3.start()
        # t1.join()
        t2.join()
        t3.join()

        result_linkedin = linkedin.filteredJobs
        result_bayt = bayt.filteredJobs
        result_google=google.filteredJobs

        print ("Scraping Finished")

        results = [*result_linkedin, *result_bayt,*result_google]
        print(results)
        return results


@eel.expose
def fetch():

    global results
    results=Database().fetch_data()
    return results






eel.init('GUI/web')
eel.start('index.html') 
