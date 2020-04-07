from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'{self.username}: {self.name}'


class ImbdContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    award = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    nominees = db.Column(db.Text, nullable=False)
    winner = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'{self.award} {self.winner}'


class Quiz(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), primary_key=True)
    score = db.Column(db.Integer, default=0)

    user = relationship('User', foreign_keys='Quiz.user_id')

    def __repr__(self):
        return f'{self.user_id}: {self.score}'


class Question():
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, ForeignKey(ImbdContent.id), primary_key=True)
    quiz_id = db.Column(db.Integer, ForeignKey(Quiz.id))
    option1 = db.Column(db.String(150), nullable=False)
    option2 = db.Column(db.String(150), nullable=False)
    option3 = db.Column(db.String(150), nullable=False)
    option4 = db.Column(db.String(150), nullable=False)
    right_answer = db.Column(db.String(10), nullable=False)
    answered = db.Column(db.String(10))

    content = relationship('ImbdContent', foreign_keys='Question.content_id')
    quiz = relationship('Question', foreign_keys='Question.quiz_id')

    def __repr__(self):
        return f'{self.right_answer}: {self.answered}'



db.create_all()

admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()

# s = db.session
# objects = [
#     User(username="u1"),
#     User(username="u2"),
#     User(username="u3")
# ]
# s.bulk_save_objects(objects)
# s.commit()