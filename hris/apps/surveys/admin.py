from django.contrib import admin

from .models import *

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['survey_id', 'survey_name', 'survey_desc', 'survey_date_posted', 'respondents']

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'survey_id', 'question_number', 'question_text']

@admin.register(SurveyOption)
class SurveyOptionAdmin(admin.ModelAdmin):
    list_display = ['option_id', 'question_id', 'option_number', 'option_text']

@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_id', 'question_id', 'employee_id', 'answer_w_option', 'answer_n_option']

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['response_id', 'survey_id', 'employee_id', 'response_date']

