from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.postImage, name='postImage'),
    url('posts/', views.PostView.as_view(), name= 'posts_list'),
    url('getprofileimage/', views.getprofileimage, name= 'getprofileimage'),
]
