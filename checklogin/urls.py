from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.checklogin, name='checklogin'),
    url(r'^checklogin/', views.checklogin, name='checklogin'),
]
