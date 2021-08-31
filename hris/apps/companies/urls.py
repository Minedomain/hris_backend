from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'companies'

router = DefaultRouter()
router.register('', CompanyViewset, basename='companies')

urlpatterns = [
    path('', include(router.urls)),
]