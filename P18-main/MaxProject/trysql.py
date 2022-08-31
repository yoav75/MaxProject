from TrtSQLFlask import db
from TrtSQLFlask import User



db.create_all()
admin = User(email='dmin@example.com', password="12345")
guest = User(username='uest', email='uest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()
