from django import template
from ..models import Subject
from ..forms import HomeworkForm

register = template.Library()

@register.simple_tag
def get_homework_form(obj):
    form = HomeworkForm(initial={
        'subject_id' : obj.pk
    })
    return form