from django.urls import path
from .views import create_quiz, show_quizzes, add_questions, add_choices, GetQuestions

urlpatterns = [
    path('',create_quiz, name='create_quiz'),
    path('shw_quiz', show_quizzes, name='show_quizzes'),
    path('add_question/<str:quiz_slug>', add_questions, name='add_question'),
    path('add_choices/<str:question_slug>/', add_choices, name='add_choices'),
    path('get_questions/<str:quiz_slug>/', GetQuestions, name='get_question'),
    # path('question_answering/<str:quiz_slug>/', QuizAnsweringView, name='question_answering'),
]
