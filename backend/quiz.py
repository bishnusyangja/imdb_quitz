import random
from sqlalchemy import desc
from flask import request, make_response, jsonify
from sqlalchemy.orm import joinedload

from helpers import get_question_text, get_options_from_content, get_random_string
from models import Quiz, Question, ImdbContent, db
from views import BaseView


class QuizView(BaseView):
    field_items = ('key_id', 'question', 'option1', 'option2', 'option3', 'option4', 'quiz_id', )

    def __init__(self, req, **kwargs):
        super().__init__(req)
        self.quiz_id = kwargs.get('quiz_id')

    def permission_for_post(self):
        try:
            quiz = Quiz.query.get(self.quiz_id)
        except Exception as exc:
            print('GetQuizExc: ', exc)
            error = {'error': 'No quiz found'}
            return False, error
        else:
            if not quiz.user_id == self.user.id:
                error = {'error': 'You have no permission to attempt this quiz'}
                return False, error
            if quiz.is_submitted:
                error = {'error': 'You have already answered this quiz'}
                return False, error
        return True, {}

    def permission_for_get(self):
        quiz_attempted = self.get_quiz_attempted()
        if quiz_attempted >= 1:
            error = {'error': 'Only one quiz can be attempted by a user'}
            return False, error
        return True, {}

    def check_permission(self):
        if self.request.method.lower() == 'get':
            return self.permission_for_get()
        if self.request.method.lower() == 'post':
            return self.permission_for_post()

    def get_question_obj(self, content, quiz_id):
        params = get_options_from_content(content)
        if params:
            obj = Question(content_id=content.id,
                           quiz_id=quiz_id,
                           key_id=get_random_string(20),
                           question=get_question_text(content),
                           **params)
        else:
            obj = None
        return obj

    def get_quiz_id(self):
        q = Quiz(user_id=self.user.id)
        db.session.add(q)
        db.session.commit()
        return q.id

    def bulk_create_questions(self, questions):
        s = db.session
        s.bulk_save_objects(questions)
        s.commit()

    def get_initial_questions(self, remaining):
        samples = random.sample(range(20), remaining)
        qs = ImdbContent.query.filter(ImdbContent.id.in_(samples))
        return qs

    def get_question_list(self):
        count = ImdbContent.query.count()
        samples = random.sample(range(count), 10)
        samples = [i+1 for i in samples]
        qs = ImdbContent.query.filter(ImdbContent.id.in_(samples))
        questions = []
        quiz_id = self.get_quiz_id()
        for content in qs:
            ques = self.get_question_obj(content, quiz_id)
            if ques:
                questions.append(ques)
        if len(questions) < 10:
            remaining = 10 - len(questions)
            rm_qs = self.get_initial_questions(remaining)
            for content in rm_qs:
                ques = self.get_question_obj(content, quiz_id)
                if ques:
                    questions.append(ques)

        self.bulk_create_questions(questions)
        return questions

    def get_queryset(self):
        return self.get_question_list()

    def get_quiz_attempted(self):
        quiz_attempted = Quiz.query.filter_by(user_id=self.user.id).count()
        return quiz_attempted

    def evaluate_quiz(self, quiz):
        score = 0
        qs = Question.query.filter_by(quiz_id=self.quiz_id).all()
        ans_dict = {item.key_id: {'answer': item.right_answer, 'id': item.id} for item in qs}
        update_list = []
        for ques, ans in quiz.items():
            if ques and ans and ans_dict.get(ques):
                update_list.append({'id': ans_dict.get(ques).get('id'), 'answered': ans})
                if ans_dict.get(ques) and ans_dict.get(ques).get('answer') == ans.strip():
                    score += 1
        db.session.bulk_update_mappings(Question, update_list)
        return score

    def save_score_on_quiz(self, score):
        obj = Quiz.query.get(self.quiz_id)
        obj.score = score
        obj.is_submitted = True
        db.session.add(obj)
        db.session.commit()

    def validate_fields(self, data):
        return {}

    def after_validation(self, data):
        score = self.evaluate_quiz(data)
        self.save_score_on_quiz(score)
        return make_response(jsonify(dict(score=score)), 200)


class ScoreView(BaseView):
    field_items = ('user.name', 'user.username', 'score', )

    def get_queryset(self):
        self.count = Quiz.query.count()
        qs = Quiz.query.options(joinedload(Quiz.user)).order_by(desc(Quiz.score)).all()
        return qs


def score_view():
    obj = ScoreView(request)
    return obj.get_response()


def quiz_view(quiz_id=None):
    obj = QuizView(request, quiz_id=quiz_id)
    return obj.get_response()