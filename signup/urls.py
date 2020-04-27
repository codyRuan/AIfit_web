from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'callback/', views.oauth_callback),
    url(r'welcome/', views.welcome),
    url(r'logout/', views.logout),
]