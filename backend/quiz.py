from flask import request
from views import BaseView


class QuizView(BaseView):

    def get(self):
        # listing quiz questions
        return True

    def post(self):
        # submitting quiz answer
        return True


class ScoreView(BaseView):
    field_items = ()

    def get_queryset(self):
        qs = []
        return qs


def score_view():
    obj = ScoreView(request)
    return obj.get_response()


def quiz_view():
    obj = QuizView(request)
    return obj.get_response()