from app import create_app, db
from app.models import User

print db

app = create_app('development')
app_context = app.app_context()
app_context.push()

user_jason = User(username='jason', password_hash='jason')
user_jason.hash_password('jason')

user_jason_2 = User(username='jason_liu', password_hash='jason_liu')
user_jason_2.hash_password('jason_liu')

db.create_all()
db.session.add(user_jason)
db.session.add(user_jason_2)
db.session.commit()

print(User.query.all())

#db.drop_all()

