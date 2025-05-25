from django.urls import path
from . import views

app_name = 'app_blog'

urlpatterns = [
    path('', views.Blog_list, name="blog_list"),
    path('create-blog/', views.CreateBlog.as_view(), name="create_blog"),
]