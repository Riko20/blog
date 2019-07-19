from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('', views.home, name='blog-home'), # changed
    path('', views.PostList.as_view(), name='blog-home'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<str:slug>/', views.PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<str:slug>/delete', views.PostDelete.as_view(), name='post_delete'),
    path('tags/', views.tag_list, name='tag_list_url'),
    path('tags/create/', views.TagCreate.as_view(), name='tag_create'),
    path('tags/<str:slug>/', views.TagDetail.as_view(), name='tag_detail_url'),
    path('tags/<str:slug>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('tags/<str:slug>/delete', views.TagDelete.as_view(), name='tag_delete'),
    path('useregistration', views.CreateUser.as_view(), name='user_create'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user_logout'),

]