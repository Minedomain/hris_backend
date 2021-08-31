from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Survey(models.Model):
  survey_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  survey_name = models.CharField(max_length=255, blank=False)
  survey_desc = models.CharField(max_length=255, blank=True, null=True, default=None)
  survey_date_posted = models.DateField(auto_now_add=True, auto_now=False, editable=False)
  respondents = models.IntegerField(default=0)

  def __str__(self):
        return 'Survey: ' + self.survey_name

class SurveyQuestion(models.Model):
  question_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
  question_number = models.IntegerField(blank=False)
  question_text = models.CharField(max_length=255, blank=False)

  def __str__(self):
        return f"Question: {self.question_number}. {self.question_text}"

class SurveyOption(models.Model):
  option_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  question_id = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
  option_number = models.IntegerField(blank=False)
  option_text = models.CharField(max_length=255, blank=False)

  def __str__(self):
        return f"Option: {self.option_number}. {self.option_text}"

class SurveyAnswer(models.Model):
  answer_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  question_id = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
  employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
  answer_w_option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE, null=True, default=None)
  answer_n_option = models.CharField(max_length=255, null=True, default=None)

class SurveyResponse(models.Model):
  response_id = models.UUIDField(default=uuid.uuid4, max_length=255, editable=False, blank=False, unique=True)
  survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
  employee_id = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
  response_date = models.DateField(auto_now_add=True, auto_now=False, editable=False)