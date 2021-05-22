from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from .models import Quiz, Question, Answer
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from urllib.parse import urlencode
from django.views.generic import (CreateView)
from .forms import QuizForm, AnswerForm, QuestionForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import (
					ListView,
					DetailView,
					CreateView,
					UpdateView,
					DetailView
	)

# Create your views here.



# NON VIEW METHODS
def stringCorrection(string):
	string = list(string)
	for i in string:
		if i=='"':
			i='\"'
		if i=="'":
			i="\'"
	temp = ""
	for i in string:
		temp+=i
	# print(temp)
	return temp


# @login_required
# def home(request):
# 	context={
# 		'quizes':Quiz.objects.all(),
# 	}
# 	return render(request, 'quiz/home.html', context)


def QuizAttempt(request, quiz_id):
	quiz = Quiz.objects.get(pk = quiz_id)
	context = {
		'quiz': quiz,
	}
	return render(request, 'quiz/quiz_attempt.html', context)

def QuizDataAttempt(request, quiz_id):
	quiz = Quiz.objects.get(pk = quiz_id)
	questions = []
	questions_id = []
	for q in quiz.get_questions():
		answers = []
		answers_id =[]
		for a in q.get_answers():
			answers.append(a.text)
			answers_id.append(a.id)
		questions.append({stringCorrection(str(q)): answers})
		questions_id.append({int(q.id): answers_id})
		# print(questions)
	return JsonResponse({
			'data': questions,
			'time': quiz.time,
			'quiz_id': quiz_id,
			'questions_id': questions_id,
		})

class QuizListView(ListView):
	model = Quiz
	template_name = 'quiz/home.html'
	context_object_name='quizes'
	ordering = ['-date_created']
	paginate_by = 10


def UserQuizes(request):
	username = User.objects.get(pk=request.user.id)
	user_quizes = Quiz.objects.filter(user=username)
	return render(request, 'quiz/user_quizes.html', {'user_quizes': user_quizes})

def UserQuizDetailView(request, quiz_id):
	quiz = Quiz.objects.get(pk=quiz_id)
	return render(request, 'quiz/user_quiz_detail.html', {'quiz': quiz})






def AddMoreQuestion(request, quiz_id):
	quiz_instance = Quiz.objects.get(pk=quiz_id)
	QuestionFormset = inlineformset_factory(Quiz, Question, fields=['text'], extra=1, can_delete=False)
	AnswerFormset = inlineformset_factory(Question, Answer, fields=['text', 'correct'], extra=4, can_delete=False)
	if request.method == 'POST':
		question_form = QuestionFormset()
		answer_form = AnswerFormset()
		question_form = QuestionFormset(request.POST, instance=quiz_instance)
		if question_form.is_valid() and question_form.has_changed():
			Question_instance = question_form[0].instance
			answer_form = AnswerFormset(request.POST, instance=Question_instance)
			if answer_form.is_valid() and answer_form.has_changed() and len(answer_form)>0:
				question_form.save()
				answer_form.save()
				messages.success(request, f'Question saved successfully!')
				if 'create_quiz_save_btn' in request.POST:
					return redirect('quiz-home')
				else:
					return redirect('add_more_question', quiz_id)
			else:
				messages.info(request, f'Empty option text!')
		else:
			messages.info(request, f"Empty question text or option text!")


			


	else:
		# quiz_form = QuizForm(initial={'time':5, 'required_score_to_pass': 1, 'difficulty': 'medium', 'topic': 'test quiz'})
		question_form = QuestionFormset()
		answer_form = AnswerFormset()

	context = {
		'quiz': quiz_instance,
		'question_form': question_form,
		'answer_form': answer_form,

	}	

	return render(request, 'quiz/add_question.html', context)





def AddQuiz(request):
	QuestionFormset = inlineformset_factory(Quiz, Question, fields=['text'], extra=1, can_delete=False)
	AnswerFormset = inlineformset_factory(Question, Answer, fields=['text', 'correct'], extra=4, can_delete=False)
	# QuizForm(initial={'time':5, 'required_score_to_pass': 1, 'difficulty': 'medium'})
	question_form = QuestionFormset()
	answer_form = AnswerFormset()
	if request.method == 'POST':
		quiz_form = QuizForm(request.POST, initial={'time':5, 'required_score_to_pass': 1, 'difficulty': 'medium', 'topic': 'test quiz'})
		if quiz_form.is_valid() and quiz_form.has_changed():
			quiz_form.instance.user = request.user
			quiz_instance = quiz_form.save().id
			quiz_id = quiz_instance
			quiz_instance = Quiz.objects.get(pk=quiz_instance)
			question_form = QuestionFormset(request.POST, instance=quiz_instance)
			if question_form.is_valid() and question_form.has_changed():
				Question_instance = question_form[0].instance
				answer_form = AnswerFormset(request.POST, instance=Question_instance)
				if answer_form.is_valid() and answer_form.has_changed() and len(answer_form)>0:
					question_form.save()
					answer_form.save()
					messages.success(request, f'Question saved successfully!')
					if 'create_quiz_save_btn' in request.POST:
						return redirect('quiz-home')
					else:
						return redirect('add_more_question', quiz_id)
				else:
					messages.info(request, f'Fill option!')
			else:
				messages.info(request, f'Fill question details')
		else:
			messages.info(request, f"Please fill all '*' marked fields while entering Quiz details")


	else:
		quiz_form = QuizForm(initial={'time':5, 'required_score_to_pass': 1, 'difficulty': 'medium', 'topic': 'test quiz'})
		question_form = QuestionFormset()
		answer_form = AnswerFormset()

	context = {
		'quiz_form': quiz_form,
		'question_form': question_form,
		'answer_form': answer_form,

	}	

	return render(request, 'quiz/quiz_create.html', context)


def save_quiz_view(request, quiz_id):
	print("request is : ", request)
	# print(request.POST)
	if request.is_ajax():
		questions = []
		data = request.POST
		data_ = dict(data.lists())
		# print(data_)
		data_.pop('csrfmiddlewaretoken')
		# print(data_)

		question_list = list(Question.objects.filter(quiz=quiz_id))
		questions = []
		
		for q in question_list:
			questions.append(q)



		# print(" ====================================================")
		# for q in questions:
		# 	print(q)
		# print(" ====================================================")
		# print(len(questions))



		# for k in data_.keys():
		# 	# print('key: ', k)
		# 	question = Question.objects.all(quiz=quiz_id)
		# 	question = list(question)
		# 	print(question.text)
			
			# questions.append(question)

		# print("         ++++++++++++++++++++++++++++++++++++++              ")
		# print(questions)
		# print("         ++++++++++++++++++++++++++++++++++++++              ")







		user = request.user
		quiz = Quiz.objects.get(pk=quiz_id)

		score = 0
		multiplier = 100/len(list(Question.objects.filter(quiz=quiz_id)))
		results = []
		correct_answer = None

		for q in questions:
			a_selected = request.POST.get(q.text)
			# print(a_selected)

			# print(type(a_selected))
			if a_selected != "" or a_selected is None:
				question_answer = Answer.objects.filter(question = q)
				for a in question_answer:
					if a_selected == a.text:
						if a.correct:
							score += 1
							correct_answer = a.text
					else:
						if a.correct:
							correct_answer = a.text

				results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
			else:
				results.append({str(q): 'not answered'})
		# for a in results:
			# print(a)
			# print("********************")

		score_ = score*multiplier
		if score_>= quiz.required_score_to_pass:
			return JsonResponse({'passed': True, 'score': score_, 'results': results})
		else:
			return JsonResponse({'passed': False, 'score': score_, 'results': results})



# def AddQuestion(request, quiz_id):
# 	quiz_instance=Quiz.objects.get(pk=quiz_id)
# 	AnswerFormset=inlineformset_factory(Question, Answer, form=AnswerForm, extra=4)
# 	if request.method == 'POST':
# 		question_form=QuestionForm(request.POST)
# 		answer_formet = AnswerFormset(request.POST)
# 		if question_form.is_valid() and answer_formet.is_valid():
# 			question_form.instance.quiz=quiz_instance
# 			question=question_form.save()
# 			answer_formet=AnswerFormset(request.POST, instance=question)
# 			if answer_formet.is_valid():
# 				answer_formet.save()
# 	else:
# 		question_form=QuestionForm()
# 		answer_formet = AnswerFormset()
	

# 	return render(request, 'quiz/add_question.html', { 'quiz_form': quiz_instance, 'question_formet':question_form, 'answer_formet':answer_formet })




# def quiz_create(request):
# 	if request.method == 'POST':
# 		form=QuizForm(request.POST)
# 		if form.is_valid():
# 			User=request.user
# 			form.instance.user=User
# 			quiz_id=form.save().id

# 			# passing id to the url
# 			# base_url=reverse('add_question')
# 			# query_string=urlencode({'question_id': quiz_id})
# 			# url='{}?{}'.format(base_url, query_string)

# 			return redirect('add_question', quiz_id)
# 	else:
# 		form=QuizForm()
# 	return render(request, 'quiz/quiz_create.html', {'form': form})
















