from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.GetDeviceToken, name='getToken'),
    url(r'^getToken/', views.GetDeviceToken, name='getToken'),
    url(r'^getMessage/', views.GetMessage, name='getMessage'),
    url(r'^deleteMessage/', views.deletMessage, name='deleteMessage'),
    url(r'^postMessage', views.postNotificationToAllUser, name='postMessage'),
]