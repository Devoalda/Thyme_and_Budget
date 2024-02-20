"""
URL configuration for thyme_and_budget project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )

urlpatterns = [path('admin/', admin.site.urls),

               # Documentation
               path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Optional UI:
               path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
               path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

               # Recipe
               # path('recipe/', include('recipe.urls')),

               # nutrition value
               # path('nutritionValue/', include('nutritionValue.urls')),

               # thyme_and_budget_app
               path('', include('thyme_and_budget_app.urls')),

               # jwt
               path('', include('account.urls')),
               path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                    document_root=settings.STATIC_ROOT)
