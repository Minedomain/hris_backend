from rest_framework import serializers
from .models import Announcement, Memo, PersonalMessage
from ..employees.models import Employee
from ..departments.models import Department

class AnnouncementSerializer(serializers.ModelSerializer):

    announce_posted_by = serializers.SlugRelatedField(slug_field='employee_id', read_only=True)
    announce_poster_name = serializers.SerializerMethodField('get_employee_name')
    announce_poster_role = serializers.SerializerMethodField('get_employee_role')
    
    class Meta:
        model = Announcement
        fields = ['announce_id', 'announce_posted_by', 'announce_poster_name', 'announce_poster_role', 'announce_subject', 'announce_content', 'announce_date']
        
    def create(self, validated_data):
        announce_posted_by = Announcement.objects.create(announce_posted_by=self.context['request'].user,
                                 **validated_data)
        return announce_posted_by
    
    def get_employee_name(self, obj):
        return obj.announce_posted_by.name
    
    def get_employee_role(self, obj):
        return obj.announce_posted_by.department_role

# Memo
class MemoSerializer(serializers.ModelSerializer):

    memo_posted_by = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)
    memo_receiver_employee = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=True)
    memo_receiver_dept = serializers.SlugRelatedField(slug_field='department_id', queryset=Department.objects.all(), allow_null=True)

    class Meta:
        model = Memo
        fields = ['memo_id', 'memo_subject', 'memo_content', 'memo_image', 'memo_posted_by', 'memo_receiver_employee', 'memo_receiver_dept', 'memo_date_created']

    def validate(self, data):
        memo_receiver_employee = data['memo_receiver_employee']
        memo_receiver_dept = data['memo_receiver_dept']
        errors = []

        try:
            if not memo_receiver_employee and not memo_receiver_dept:
                errors.append('Choose between employee, department, or both as recipient.')
            else:
                pass

        except Memo.DoesNotExist:
            errors.append('Employee/Department does not exists.')

        if len(errors):
            error_message = {'errors': errors}
            raise serializers.ValidationError(error_message)

        return data

# Message
class PersonalMessageSerializer(serializers.ModelSerializer):

    message_sender = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)
    message_receiver = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = PersonalMessage
        fields = ['message_id', 'message_sender', 'message_receiver', 'message_details', 'message_date_sent', 'message_is_read']

class PersonalMessageCreateSerializer(serializers.ModelSerializer):

    message_sender = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)
    message_receiver = serializers.SlugRelatedField(slug_field='employee_id', queryset=Employee.objects.all(), allow_null=False)

    class Meta:
        model = PersonalMessage
        fields = ['message_id', 'message_sender', 'message_receiver', 'message_details', 'message_date_sent']