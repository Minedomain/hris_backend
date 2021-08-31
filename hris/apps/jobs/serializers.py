from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_id', 'job_title', 'duties', 'min_salary', 'max_salary']

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_title', 'duties', 'min_salary', 'max_salary']

    def validate(self, data):
        job_title = data['job_title']

        try:
            Job.objects.get(job_title=job_title)
            raise serializers.ValidationError({'error': "Job Title already exists!"})
        except Job.DoesNotExist:
            pass

        data['job_title'] = job_title
        
        return data

    def create(self, validated_data):
        job_title = validated_data['job_title']
        duties = validated_data['duties']
        min_salary = validated_data['min_salary']
        max_salary = validated_data['max_salary']

        return Job.objects.create(
            job_title= job_title,
            duties = duties,
            min_salary = min_salary,
            max_salary = max_salary
        )
        

    