from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.history, name='history'),
    url(r'^addwork/', views.addwork, name='addwork'),
    url(r'^history/', views.history, name='history'),
    url(r'^history_api/', views.api_history, name='history_api'),
]