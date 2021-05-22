from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random

# Create your models here.

class Quiz(models.Model):

	choices={
		('easy', 'easy'),
		('medium', 'medium'),
		('hard', 'hard'),
	}

	title=models.CharField(max_length=100)
	topic=models.CharField(max_length=100)
	date_created=models.DateTimeField(auto_now=True)
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	time=models.IntegerField(help_text='duration of the quiz in mins')
	required_score_to_pass=models.IntegerField(help_text='required score to pass.')
	difficulty=models.CharField(max_length=6, choices=choices)

	def __str__(self):
		return self.title

	def get_questions(self):
		questions = list(self.question_set.all())
		random.shuffle(questions)
		return questions

	def get_question_count(self):
		count = len(self.question_set.all())
		return count

	class Meta:
		verbose_name_plural='quizes'


class Question(models.Model):
	text=models.TextField()
	quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

	def get_answers(self):
		return self.answer_set.all()


class Answer(models.Model):
	text=models.CharField(max_length=200)
	correct=models.BooleanField(default=False)
	question=models.ForeignKey(Question, on_delete=models.CASCADE)

	def __str__(self):
		return f'quiz: {self.question.quiz.title} ques: {self.question.text}, ans: {self.text}, correct: {self.correct}'

