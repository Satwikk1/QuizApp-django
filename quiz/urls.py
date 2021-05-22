from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.QuizListView.as_view(), name='quiz-home'),
	path('quiz_create/', views.AddQuiz, name="quiz_create"),
	path('add_question/<int:quiz_id>/', views.AddMoreQuestion, name='add_more_question'),
	path('user_quiz_detail/<int:quiz_id>/', views.UserQuizDetailView, name='user_quiz_detail'),
	path('user_quizes/', views.UserQuizes, name='user_quizes'),
	path('quiz_attempt/<int:quiz_id>/', views.QuizAttempt, name='quiz_attempt'),
	path('quiz_attempt/<int:quiz_id>/data/save/', views.save_quiz_view, name='save_quiz_view'),
	path('quiz_attempt/<int:quiz_id>/data/', views.QuizDataAttempt, name='quiz_data_attempt'),
]