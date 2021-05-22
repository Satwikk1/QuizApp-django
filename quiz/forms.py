from django import forms
from .models import *

class QuizForm(forms.ModelForm):

	class Meta:
		model=Quiz
		fields=['title', 'topic', 'time', 'required_score_to_pass', 'difficulty']

class QuestionForm(forms.ModelForm):
	class Meta:
		model=Question
		fields=['text']

class AnswerForm(forms.ModelForm):
	class Meta:
		model=Answer
		fields=['text', 'correct']