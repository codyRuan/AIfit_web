
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.lineup, name='lineup'),
    url(r'^join/', views.join, name='join'),
    url(r'^leave/', views.leave, name='leave'),
    url(r'^getQstatus/', views.getQstatus, name='getQstatus'),
    url(r'^StartWorkout/', views.StartWorkout, name='StartWorkout'),
    url(r'^GetTimer/', views.GetTimer, name='GetTimer'),
    url(r'^forvideo/', views.forvideo, name='forvideo'),
    
]