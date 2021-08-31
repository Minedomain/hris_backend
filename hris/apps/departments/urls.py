from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'departments'

router = DefaultRouter()
router.register('', DepartmentViewset, basename='departments')

urlpatterns = [
    path('', include(router.urls)),
]