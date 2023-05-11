from django import template

from first_tour.models import ExamSubject, ExamResult

register = template.Library()


@register.filter(name="final_score")
def final_score(value: ExamResult):
    score = value.score
    if value.appeal_score:
        score = value.appeal_score
    return score
