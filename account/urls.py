from django.urls import path, include


from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    UserListView,
    LogoutView,
)
# router = DefaultRouter()
# router.register(r'token/obtain/', jwt_views.TokenObtainPairView, basename='token_obtain_pair')
# router.register(r'token/refresh/', jwt_views.TokenRefreshView, basename='token_refresh')
# router.register(r'register', AuthUserRegistrationView.as_view(), basename='register')
# router.register(r'login', AuthUserLoginView.as_view(), basename='login')
# router.register(r'users', UserListView.as_view(), basename='users')

urlpatterns = [
    # path('', include(router.urls)),
    # path('register', RegisterApi.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', AuthUserRegistrationView.as_view(), name='register'),
    path('login/', AuthUserLoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users')
]
