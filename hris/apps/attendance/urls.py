from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'attendance'

router = DefaultRouter()
router.register('', AttendanceViewset, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
    path('employee', AttendanceRetrieveView.as_view(), name='attendance-retrieve'),
]