"""config URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import Home

schema_view = get_schema_view(
    openapi.Info(
                title='Superliga',
                description='django rest frameworkda futbo, sayti',
                default_version='1.0.0',
                contact=openapi.Contact(email='freejobmakery@gmail.com'),
                license=openapi.License(name='Online result litsenziyasi')
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('club/', include('clubs.urls')),
    path('news/', include('news.urls')),
    path('api/', include('api.urls')),
    path('account/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/dj-rest-auth/register/', include('dj_rest_auth.registration.urls')),
    path('api/allauth/', include('allauth.urls')),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='swagger-schema-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='redoc-schema-ui'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

