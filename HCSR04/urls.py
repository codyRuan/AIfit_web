from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HCSR04View.as_view()),
]
