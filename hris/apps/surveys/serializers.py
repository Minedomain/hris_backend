from rest_framework import serializers
from .models import *
from ..employees.models import Employee

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['survey_id', 'survey_name', 'survey_desc', 'survey_date_posted', 'respondents']

# Question
class SurveyQuestionSerializer(serializers.ModelSerializer):

    survey_id = serializers.SlugRelatedField(slug_field='survey_id', queryset=Survey.objects.all(), allow_null=False)

    class Meta:
        model = SurveyQuestion
        fields = ['question_id', 'survey_id', 'question_number', 'question_text']

class SurveyQuestionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = ['question_number', 'question_text']

# Options
class SurveyOptionSerializer(serializers.ModelSerializer):

    question_id = serializers.SlugRelatedField(slug_field='question_id', queryset=SurveyQuestion.objects.all(), allow_null=False)

    class Meta:
        model = SurveyOption
        fields = ['option_id', 'question_id', 'option_number', 'option_text']

class SurveyOptionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ['option_number', 'option_text']

# Answer
class SurveyAnswerSerializer(serializers.ModelSerializer):

    question_id = serializers.SlugRelatedField(slug_field='question_id', queryset=SurveyQuestion.objects.all(), allow_null=False)
    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=True)
    answer_w_option = serializers.SlugRelatedField(slug_field='option_id', queryset=SurveyOption.objects.all(), allow_null=True)

    class Meta:
        model = SurveyAnswer
        fields = ['answer_id', 'question_id', 'employee_id', 'answer_w_option', 'answer_n_option']

    def validate(self, data):
        answer_w_option = data['answer_w_option']
        answer_n_option = data['answer_n_option']
        errors = []

        try:
            if not answer_w_option and not answer_n_option:
                errors.append('Answer has not been chosen.')
            elif answer_w_option and answer_n_option:
                errors.append('Choose one option only.')
            else:
                pass

        except SurveyAnswer.DoesNotExist:
            errors.append('Employee/Department does not exists.')

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

class SurveyAnswerRetrieveSerializer(serializers.ModelSerializer):
    answer_w_option = serializers.SlugRelatedField(slug_field='option_id', queryset=SurveyOption.objects.all(), allow_null=True)
    class Meta:
        model = SurveyAnswer
        fields = ['answer_w_option', 'answer_n_option']

# Response
class SurveyResponseSerializer(serializers.ModelSerializer):

    survey_id = serializers.SlugRelatedField(slug_field='survey_id', queryset=Survey.objects.all(), allow_null=False)
    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = SurveyResponse
        fields = ['survey_id', 'employee_id', 'response_date']