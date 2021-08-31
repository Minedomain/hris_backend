from django.contrib import admin

from .models import *

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["announce_id", "announce_posted_by", "announce_subject", "announce_content", "announce_date"]

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['memo_id', 'memo_subject', 'memo_content', 'memo_image', 'memo_posted_by', 'memo_receiver_employee', 'memo_receiver_dept', 'memo_date_created']

@admin.register(PersonalMessage)
class PersonalMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'message_sender', 'message_receiver', 'message_details', 'message_date_sent', 'message_is_read']

