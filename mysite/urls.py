"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from its_regions_2025.views import (
    AuthenticatedAPIView,
    LoginViewSet,
    LogoutViewSet,
    RegistrationViewSet,
)

urlpatterns = [
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("admin/", admin.site.urls),
    path("api/v1/auth/", AuthenticatedAPIView.as_view(), name="auth"),
    path("api/v1/login/", LoginViewSet.as_view(), name="login"),
    path("api/v1/register/", RegistrationViewSet.as_view(), name="register"),
    path("api/v1/logout/", LogoutViewSet.as_view(), name="logout"),
    path("api/v1/", include("its_regions_2025.urls"), name="api"),
    # Yaml openapi
    path("api/v1/openapi/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
