import eel
import time
from threading import Thread

result =[]

def test1 ():
    global result
    for x in range(10):
        time.sleep(1)
        temp = f"test1 {x}"
        result.append(temp)

def test2 ():
    global result
    for x in range(10):
        time.sleep(1)
        temp = f"test2 {x}"
        result.append(temp)

@eel.expose
def startScrapping():
    t1 = Thread(target=test1, args=())
    t2 = Thread(target=test2, args=())
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    global result
    return result
    
def start_scrapping(data):
        pass
"""
        # title = data.title
        # keyworsd = data.keywords
        # country = data.country
        # city = data.city


        # threads = []




        # t = Thread(...)
        # threads.append(t)



        # # Start all threads
        # for x in threads:
        #     x.start()

        # # Wait for all of them to finish
        # for x in threads:
        #     x.join()



#     linkedin = Linkedin(title,location,skills)
#     bayt = bayt(title,location,skills)
#     gulf = gulf(title,location,skills)
#     nukkri = nukkri(title,location,skills)

#     prepare_results(linked.filterdjobs)
#     prepare_results(bayt.filterdjobs)
#     prepare_results(gulf.filterdjobs)
#     prepare_results(nukkri.filterdjobs)
#     return result
"""



eel.init('GUI/web')
eel.start('index.html') 