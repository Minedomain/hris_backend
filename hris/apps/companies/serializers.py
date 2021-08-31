from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'company_description', 'company_address']

    def validate(self, data):
        company_name = data['company_name']

        try:
            Company.objects.get(company_name=company_name)
            raise serializers.ValidationError({'error': "Company Name already exists!"})
        except Company.DoesNotExist:
            pass

        data['company_name'] = company_name
        
        return data

    def create(self, validated_data):
        company_name = validated_data['company_name']
        company_description = validated_data['company_description']
        company_address = validated_data['company_address']

        return Company.objects.create(
            company_name= company_name,
            company_description = company_description,
            company_address = company_address
        )