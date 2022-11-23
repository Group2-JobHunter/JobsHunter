import eel
import time
from threading import Thread
 
from Scrapping.Linkedin import LinkedIn
from Scrapping.bayt import Bayt
from Scrapping.database import Database
from Scrapping.google import Google
from Scrapping.naukrigulf import Naukrigulf
from Scrapping.gulftalent import GulfTalent
from timeit import default_timer as timer
import csv
results =[]



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
        naukrigulf = Naukrigulf(title,city,country,keywords)
        gulftalent = GulfTalent(title,country,city,keywords)


        start = timer()

        t1 = Thread(target=linkedin.start, args=())
        t2 = Thread(target=bayt.start, args=())
        t3 = Thread(target=google.start, args=())
        t4 = Thread(target=naukrigulf.start, args=())
        t5 = Thread(target=gulftalent.start, args=())

        # t4.start()
        # t4.join()

        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        end = timer()
        
        result_linkedin = linkedin.filteredJobs
        result_bayt = bayt.filteredJobs
        result_google=google.filteredJobs
        result_naukri = naukrigulf.filteredJobs
        result_gulf = gulftalent.filteredJobs
        print ("Scraping Finished")
        results = [*result_linkedin, *result_bayt,*result_google,*result_naukri, *result_gulf]
        print(int(end - start))
        return results


@eel.expose
def fetch():

    global results
    db=Database()
    results = db.fetch_data()
    return results

@eel.expose
def resultsToCsv():
    tableColums = [
    "Source",
    "Title",
    "Company",
    "Date",
    "City",
    "Country",
    "Matching",
    "Poster",
  ]

    global results

    if len(results) == 0:
        return

    with open('./result.csv', 'w') as f:
    
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(tableColums)
        write.writerows(results)





eel.init('GUI/web')
eel.start('index.html') 
