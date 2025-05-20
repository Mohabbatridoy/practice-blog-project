from django.urls import path
from . import views

app_name = 'app_login'

urlpatterns = [
    path('sign_up/', views.SignUp, name="sign_up"),
    path('log_in/', views.LogIn, name="log_in"), 
    path('log_out/', views.LogOut, name="log_out"),
    path('profile/', views.Profile, name="profile"),
    path('edit_prifle/', views.EditProfile, name="edit_profile"),
    path('password/', views.Passchange, name="pass_edit")
]