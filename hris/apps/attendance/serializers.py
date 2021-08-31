from rest_framework import serializers
from .models import Attendance
from ..employees.models import Employee

class AttendanceSerializer(serializers.ModelSerializer):

    employee_id = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = Attendance
        fields = ['attendance_id', 'employee_id', 'datetime_in', 'datetime_out', 'hours_logged', 'absent']