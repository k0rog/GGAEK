from django import forms
from captcha.fields import CaptchaField
from .models import FeedbackMessage


grades = (
    (1, 'Ужасно'),
    (2, 'Плохо'),
    (3, 'Нормально'),
    (4, 'Хорошо'),
    (5, 'Отлично')
)


class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField()
    evaluation = forms.ChoiceField(choices=grades)

    class Meta:
        fields = ['name', 'email', 'subject', 'text']
        model = FeedbackMessage
