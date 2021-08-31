from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'leaves'

router = DefaultRouter()
router.register('', LeaveViewset, basename='leave')


urlpatterns = [
    path('', include(router.urls)),
    path('employee', LeaveRetrieveView.as_view(), name='leave-retrieve'),
    path('list-own', LeaveListSpecificView.as_view(), name='leave-list-own'),
    path('list-requests', LeaveListRequestsView.as_view(), name='leave-list-requests')
]