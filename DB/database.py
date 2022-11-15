import sqlite3
data={'jobtitle': 'Sr. Front End Engineer', 'location': 'Amman, Jordan','date': '30+ days ago',  'company': 'Bayt.com', 'link': 'https://www.bayt.com/en/Jordan/jobs/moderator-jobs/?jobId=4600323'}

db=sqlite3.connect('app.db')

cr=db.cursor()

cr.execute('create table if not exists Jobs (Title text,Location text, Date text, Company text,Link text )')

#inserting data



cr.execute('''INSERT INTO Jobs VALUES (:jobtitle, :location, :date,:company,:link)''',data)



db.commit()


db.close()

