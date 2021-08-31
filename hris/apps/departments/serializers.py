from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name', 'department_details']

class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name', 'department_details']

    def validate(self, data):
        department_name = data['department_name']

        try:
            Department.objects.get(department_name=department_name)
            raise serializers.ValidationError({'error': "Department Name already exists!"})
        except Department.DoesNotExist:
            pass

        data['department_name'] = department_name
        
        return data

    def create(self, validated_data):
        department_name = validated_data['department_name']
        department_details = validated_data['department_details']

        return Department.objects.create(
            department_name= department_name,
            department_details = department_details,
        )