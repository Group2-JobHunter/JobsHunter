import sqlite3



class Database():

  
        

    db = sqlite3.connect('app.db',check_same_thread=False)
    cr = db.cursor()
    
    
    def save_data(self,data):
        Database.cr.execute(
            'create table if not exists Jobs (Source text,Title text, Company text, Date text,City text,Country text,Percatnage text,Link text)')

        
        Database.cr.executemany("INSERT or REPLACE into Jobs VALUES (?,?,?,?,?,?,?,?)",data)
        Database.db.commit()
        # Database.db.close()

    def fetch_data(self):
        
      
        Database.cr.execute('select * from Jobs')
        results = Database.cr.fetchall()
        # Database.db.close()

        return results
