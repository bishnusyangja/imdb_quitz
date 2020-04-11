from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import get_core_app
from helpers import hash_password, verify_password
from settings import DB_NAME, DB_PATH

app = get_core_app()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}{DB_NAME}'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'{self.username}: {self.name}'

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(self.password, password)


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id))

    user = relationship('User', foreign_keys='UserToken.user_id')

    def __repr__(self):
        return f'{self.id} {self.token}'


class ImdbContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    award = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    nominees = db.Column(db.Text, nullable=False)
    winner = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'{self.award} {self.winner}'


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id))
    score = db.Column(db.Integer, default=0)

    user = relationship('User', foreign_keys='Quiz.user_id')

    def __repr__(self):
        return f'{self.user_id}: {self.score}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, ForeignKey(ImdbContent.id))
    question = db.Column(db.Text)
    quiz_id = db.Column(db.Integer, ForeignKey(Quiz.id))
    option1 = db.Column(db.String(150), nullable=False)
    option2 = db.Column(db.String(150), nullable=False)
    option3 = db.Column(db.String(150), nullable=False)
    option4 = db.Column(db.String(150), nullable=False)
    right_answer = db.Column(db.String(10), nullable=False)
    answered = db.Column(db.String(10), nullable=True)

    content = relationship('ImdbContent', foreign_keys='Question.content_id')
    quiz = relationship('Quiz', foreign_keys='Question.quiz_id')

    def __repr__(self):
        return f'{self.right_answer}: {self.answered}'

