from WebApp import app, db
from WebApp.models import Manager
#INSERT USERS
app.app_context().push()
'''u = Manager(id=4, name='john', email='john@example.com', password="password")
db.session.add(u)
db.session.commit()


#Test
print(u.get_password("bobpass"))
print(u.get_password("notbobpass"))

'''
#SELECT USERS
user = Manager.query.get(1)
print(user)

users = Manager.query.all()

for u in users:
    print(u.id, u.name)

#u = User(username='susan', email='susan@example.com')
#db.session.add(u)
#db.session.commit()
