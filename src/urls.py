"""Self_Help URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from Self_Help.views import TestModelView, HomePage, StandardPage, verify_account, SignUp

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

] + i18n_patterns(
    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # admin controls
    path('admin/', admin.site.urls),
    #
    path('api-auth/', include('rest_framework.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
    path('testview/', TestModelView.as_view()),
    path('home/', HomePage.as_view(), name='home'),
    path('', StandardPage.as_view()),
    path('signup/<str:short_error_message>/<str:error_message>', SignUp.as_view(), name='signup_with_error'),
    path('signup/', SignUp.as_view(), name='sign_up'),
    path('verify/<str:uid>/<str:token>', verify_account, name='verify_account'),
    prefix_default_language=False,
)
