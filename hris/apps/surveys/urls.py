from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'surveys'

router = DefaultRouter()
router.register('list', SurveyViewset, basename='survey')
router.register('questions', SurveyQuestionViewset, basename='survey-question')
router.register('options', SurveyOptionViewset, basename='survey-option')
router.register('answers', SurveyAnswerViewset, basename='survey-answer')
router.register('responses', SurveyResponseViewset, basename='survey-responses')

urlpatterns = [
    path('', include(router.urls)),
    path('questions', SurveyQuestionRetrieveView.as_view(), name='survey-question-retrieve'),
    path('options', SurveyOptionRetrieveView.as_view(), name='survey-option-retrieve'),
    path('answers', SurveyAnswerRetrieveView.as_view(), name='survey-answer-retrieve'),
    path('responses', SurveyResponseRetrieveView.as_view(), name='survey-response-retrieve'),
]