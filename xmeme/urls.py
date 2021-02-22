"""xmeme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

schema_view = get_swagger_view(title='XMeme')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', schema_view),
    path('', include('xmeme_backend.urls')),
    path('openapi/', get_schema_view(
        title="Meme Stream ",
        description="API for meam stream application",
        url='https://127.0.0.1:8080/',
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
         extra_context={'schema_url': 'openapi-schema'}
         ), name='swagger-ui'),

]
urlpatterns += staticfiles_urlpatterns()
