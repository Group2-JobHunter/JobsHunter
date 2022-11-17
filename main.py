import eel



@eel.expose

def get_python():
    
   return ['title','job','a','b','d']


search_data = {}


@eel.expose
def get_search_data(data):
    global search_data
    search_data = data

result = []

# def prepare_results(list):
#     global result

#     for job in list:
#         result.append(job)


isBusy = False
 
 def start_scrapping(data):

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



 
    
    


    





eel.init('GUI/web')
eel.start('index.html') 