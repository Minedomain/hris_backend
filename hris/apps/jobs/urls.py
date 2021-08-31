from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'jobs'

router = DefaultRouter()
router.register('', JobViewset, basename='jobs')

urlpatterns = [
    path('', include(router.urls)),
]