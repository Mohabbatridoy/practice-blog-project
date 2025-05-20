from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index , name="index"),
    path('account/', include('app_login.urls')),
    path('blog/', include('app_blog.urls')),
]
