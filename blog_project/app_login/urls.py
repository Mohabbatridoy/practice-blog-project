from django.urls import path
from . import views

app_name = 'app_login'

urlpatterns = [
    path('sign_up/', views.SignUp, name="sign_up"),
    path('log_in/', views.LogIn, name="log_in"), 
    path('log_out/', views.LogOut, name="log_out"),
    path('profile/', views.UserProfileDetails.as_view(), name="profile"),
]