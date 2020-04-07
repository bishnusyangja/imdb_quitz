import random
from flask import request, make_response, jsonify
from models import Quiz, Question, ImdbContent, db
from views import BaseView


class QuizView(BaseView):
    field_items = ()

    def check_permission(self):
        quiz_attempted = self.get_quiz_attempted()
        if quiz_attempted >= 1:
            error = {'error': 'Only one quiz can be attempted by a user'}
            return False, error
        return True, {}

    def get_question_obj(self, content, quiz_id):
        obj = Question()
        return obj

    def get_quiz_id(self):
        user_id = None
        q = Quiz(user_id=user_id)
        db.session.add(q)
        db.session.commit()
        return q.id

    def bulk_create_questions(self, questions):
        s = db.session
        s.bulk_save_objects(questions)
        s.commit()

    def get_question_list(self):
        count = ImdbContent.objects.all().count()
        samples = random.sample(range(count), 10)
        qs = ImdbContent.objects.filter(id__in=samples)
        questions = []
        quiz_id = self.get_quiz_id()
        for content in qs:
            questions.append(self.get_question_obj(content, quiz_id))
        self.bulk_create_questions(questions)
        return []

    def get_queryset(self):
        return self.get_question_list()

    def get_quiz_attempted(self):
        user_id = None
        quiz_attempted = Quiz.objects.filter(user_id=user_id).count()
        return quiz_attempted

    def evaluate_quiz(self, quiz_id):
        score = 5
        return score

    def save_score_on_quiz(self):
        pass

    def after_validation(self, data):
        quiz_id = data.get('id')
        score = self.evaluate_quiz(quiz_id)
        self.save_score_on_quiz()
        return make_response(jsonify(dict(score=score)), 200)


class ScoreView(BaseView):
    field_items = ()

    def get_queryset(self):
        qs = Quiz.objects.all()
        return qs


def score_view():
    obj = ScoreView(request)
    return obj.get_response()


def quiz_view():
    obj = QuizView(request)
    return obj.get_response()