from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('signup/', views.signup, name='signup'),
]