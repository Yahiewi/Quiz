# quiz/urls.py
from django.urls import path
from .views import QuestionList, GenerateQuizView

urlpatterns = [
    path('api/questions/', QuestionList.as_view(), name='question-list'),
    path('api/generate-quiz/', GenerateQuizView.as_view(), name='generate-quiz'),
]