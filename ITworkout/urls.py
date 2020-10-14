"""ITworkout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView


    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('record/', include('record.urls')),
    path('hcsr04/', include('HCSR04.urls')),
    path('home/', include('signup.urls')),
    path('lineup/', include('lineup.urls')),
    path('counting/', include('counting.urls')),
    path('postimage/', include('postimage.urls')),
    path('checklogin/', include('checklogin.urls')),
    path('oauth/', include('signup.urls')),
    path('notification/',include('notification.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('chat/', include('chat.urls')),
]

urlpatterns += staticfiles_urlpatterns()
