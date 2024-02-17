from django.urls import path
from .views import RegisterApi, UserApi

urlpatterns = [
    path('register', RegisterApi.as_view(), name='register'),
    path('logout', UserApi.as_view(), name='logout'),
]
