from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^setcount/', views.setcount, name='setcount'),
    url(r'^detectuser/', views.detectuser, name='detectuser'),  
    url(r'^getcurrentset/', views.getcurrentset, name='getcurrentset'),  
    url(r'^fortest/', views.fortest, name='fortest'), 
    
]