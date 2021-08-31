from rest_framework import serializers
from .models import Leave
from ..employees.models import Employee

class LeaveSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', read_only=True)

    class Meta:
        model = Leave
        fields = ['leave_id', 'employee_id', 'leave_type', 'leave_reason', 'date_filed', 'leave_status']
    
    def create(self, validated_data):
        employee_id = Leave.objects.create(employee_id=self.context['request'].user, **validated_data)
        return employee_id

class LeaveUpdateSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', read_only=True)

    class Meta:
        model = Leave
        fields = ['leave_id', 'employee_id', 'leave_type', 'leave_reason', 'date_filed', 'leave_status']
        read_only_fields = ['leave_id', 'employee_id', 'leave_type', 'leave_reason', 'date_filed']
        
class LeaveListSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)
    employee_number = serializers.SerializerMethodField('get_employee_number')
    name = serializers.SerializerMethodField('get_employee_name')
    sick_leave_count = serializers.SerializerMethodField('get_employee_sick_leave_count')
    vac_leave_count = serializers.SerializerMethodField('get_employee_vac_leave_count')

    class Meta:
        model = Leave
        fields = ['leave_id', 'employee_id', 'employee_number', 'name', 'sick_leave_count', 'vac_leave_count', 'leave_type', 'leave_reason', 'date_filed', 'leave_status' ]
    
    def get_employee_number(self, obj):
        return obj.employee_id.username
    
    def get_employee_name(self, obj):
        return obj.employee_id.name
    
    def get_employee_sick_leave_count(self, obj):
        return obj.employee_id.sick_leave_count
    
    def get_employee_vac_leave_count(self, obj):
        return obj.employee_id.vac_leave_count