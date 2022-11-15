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
 
# def start_scrapping(data):

#     location = data.location
#     keyworsd = data.keywords
#     country = data.country
#     city = data.city

    

#     linked = Linked(data)
#     bayt = bayt(data)
#     gulf = gulf(data)
#     nukkri = nukkri(data)
#     while (linked.isBusy or bayt.isBusy or gulf.isBusy or nukkri.isBusy):
#         pass
#     prepare_results(linked.filterdjobs)
#     prepare_results(bayt.filterdjobs)
#     prepare_results(gulf.filterdjobs)
#     prepare_results(nukkri.filterdjobs)
#     return result



 
    
    


    





eel.init('GUI/web')
eel.start('index.html') 