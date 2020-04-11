import random
from sqlalchemy import desc
from flask import request, make_response, jsonify
from models import Quiz, Question, ImdbContent, db
from settings import NOMINEES_SPLIT
from views import BaseView


class QuizView(BaseView):
    field_items = ('question', 'option1', 'option2', 'option3', 'option4', 'quiz_id', )

    def __init__(self, request, **kwargs):
        super().__init__(request)
        self.quiz_id = kwargs.get('quiz_id')
        print('at quiz view', self.user.id)

    def permission_for_post(self):
        try:
            print(self.quiz_id)
            quiz = Quiz.query.get(self.quiz_id)
        except Exception as exc:
            print('GetQuizExc: ', exc)
            error = {'error': 'No quiz found'}
            return False, error
        else:
            if not quiz.user_id == self.user.id:
                error = {'error': 'You have no permission to attempt this quiz'}
                return False, error
        return True, {}

    def permission_for_get(self):
        quiz_attempted = self.get_quiz_attempted()
        quiz_attempted = 0 # for testing purpose
        print('quiz attempted', quiz_attempted)
        if quiz_attempted >= 1:
            error = {'error': 'Only one quiz can be attempted by a user'}
            return False, error
        return True, {}

    def check_permission(self):
        if self.request.method.lower() == 'get':
            return self.permission_for_get()
        if self.request.method.lower() == 'post':
            return self.permission_for_post()

    def get_question_text(self, content):
        return f"Which of the following is awarded as {content.category} in {content.award} award?"

    def get_options(self, content, right_number=None):
        try:
            options = random.sample(content.nominees.replace(content.winner, '').strip(NOMINEES_SPLIT).replace(
                NOMINEES_SPLIT * 2, NOMINEES_SPLIT).split(NOMINEES_SPLIT), 3)
        except Exception as exc:
            print('Excep', exc)
            return None
        right_number = random.choice(range(4)) + 1 if right_number is None else right_number
        params = {f'option{right_number}': content.winner}
        right_assigned = False
        right_option = ''
        for i in range(3):
            if i + 1 == right_number:
                right_assigned = True
            index = i + 2 if right_assigned else i + 1
            params[f'option{index}'] = options[i]
        params['right_answer'] = right_option
        return params

    def get_question_obj(self, content, quiz_id):
        params = self.get_options(content)
        if params:
            obj = Question(content_id=content.id,
                           quiz_id=quiz_id,
                           question=self.get_question_text(content),
                           **params
                           )
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
        ans_dict = {item['id']: item['right_answer'] for item in qs}
        for question in quiz:
            ques = question.get('question')
            ans = question.get('answer')
            if ans and ans_dict.get(ques) == ans:
                score += 1
        return score

    def save_score_on_quiz(self, score):
        obj = Quiz.query.get(self.quiz_id)
        obj.score = score
        db.session.add(obj)
        db.session.commit()

    def after_validation(self, data):
        quiz = data.get('quiz')
        score = self.evaluate_quiz(quiz)
        self.save_score_on_quiz(score)
        return make_response(jsonify(dict(score=score)), 200)


class ScoreView(BaseView):
    field_items = ('user_id', 'score', )

    def get_query_limit(self):
        page = self.request.args.get('page') or self.page
        page_size = self.request.args.get('page_size') or self.page_size
        start = (page - 1) * page_size
        end = page_size * page
        return start, end

    def get_paginated_query(self, qs):
        start, end = self.get_query_limit()
        return qs[start, end]

    def get_queryset(self):
        qs = Quiz.query.all().order_by(desc(Quiz.score))
        qs = self.get_paginated_query(qs)
        return qs


def score_view():
    obj = ScoreView(request)
    return obj.get_response()


def quiz_view(quiz_id=None):
    obj = QuizView(request, quiz_id=quiz_id)
    return obj.get_response()