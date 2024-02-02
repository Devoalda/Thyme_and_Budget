from django.urls import path
from .api import RegisterApi, UserApi

urlpatterns = [
    path('register', RegisterApi.as_view(), name='register'),
    path('logout', UserApi.as_view(), name='logout'),
]
