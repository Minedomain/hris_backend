from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'engagements'

router = DefaultRouter()
router.register('announcement', AnnouncementViewset, basename='announcement')
router.register('memo', MemoViewset, basename='memo')
router.register('message', PersonalMessageViewset, basename='personal-message')

urlpatterns = [
    path('', include(router.urls)),
    path('announcement/employee', AnnouncementRetrieveView.as_view(), name='announcement-retrieve'),
    path('memo/sender', MemoSenderRetrieveView.as_view(), name='memo-sender-retrieve'),
    path('memo/receiver', MemoReceiverRetrieveView.as_view(), name='memo-receiver-retrieve'),
    path('message/sender', PersonalMessageSenderRetrieveView.as_view(), name='message-sender-retrieve'),
    path('message/receiver', PersonalMessageReceiverRetrieveView.as_view(), name='message-receiver-retrieve'),
    path('message/list-own', PersonalMessageListSpecificView.as_view(), name='message-retrieve-own'),
]