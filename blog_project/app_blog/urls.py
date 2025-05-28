from django.urls import path
from . import views

app_name = 'app_blog'

urlpatterns = [
    path('', views.Blog_list.as_view(), name="blog_list"),
    path('create-blog/', views.CreateBlog.as_view(), name="create_blog"),
    path('details/<path:slug>/', views.BlogDetails, name="blog_details"),
    path('liked/<pk>/', views.Liked, name="like_post"),
    path('unliked/<pk>/', views.Unliked, name="unlike_post"),
]