from django.urls import path

from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    UserRetrieveUpdateDestroyView,
    LogoutView,
    CheckUserLoginView,
)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', AuthUserRegistrationView.as_view(), name='register'),
    path('login/', AuthUserLoginView.as_view(), name='login'),
    path('user/', UserRetrieveUpdateDestroyView.as_view(), name='users'),
    path('check_user_login/', CheckUserLoginView.as_view(), name='check_user_login')
]
