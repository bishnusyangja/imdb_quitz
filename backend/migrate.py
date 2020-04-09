from models import User, Quiz, Question, ImdbContent, db
db.drop_all()
db.create_all()
