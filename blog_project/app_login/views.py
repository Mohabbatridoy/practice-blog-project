from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, View, TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile

# Create your views here.
def SignUp(request):
    form = forms.Usercreate()
    registered = False
    if request.method == 'POST':
        form = forms.Usercreate(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    return render(request, 'sign_up.html', context={'form':form, 'registered':registered})

def LogIn(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('app_blog:blog_list'))
    return render(request, 'log_in.html', context={'form':form,})

@login_required
def LogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('app_blog:blog_list'))



@login_required
def Profile(request):
    return render(request, 'Profile.html', context={})

@login_required
def EditProfile(reqeust):
    current_user = reqeust.user
    form = forms.UserProfileEdit(instance=current_user)
    if reqeust.method == 'POST':
        form = forms.UserProfileEdit(reqeust.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = forms.UserProfileEdit(instance=current_user)
            return HttpResponseRedirect(reverse('app_login:profile'))

    return render(reqeust, 'profile_edit.html', context={'form':form})

@login_required
def Passchange(request):
    changed = False
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            form = PasswordChangeForm(current_user)
            changed=True
    
    return render(request, 'pass_edit.html', context={'form':form, 'changed':changed})

@login_required
def ProfilePic(request):
    form = forms.ProfilePicForm()
    if request.method == 'POST':
        form = forms.ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    return render(request, 'profile_pic_form.html', context={'form':form})

@login_required
def changeProfilePic(request):
    form = forms.ProfilePicForm(instance=request.user.user_profile)
    if request.method=='POST':
        form = forms.ProfilePicForm(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app_login:profile'))
    return render(request, 'profile_pic_form.html', context={'form':form})

@login_required
def delProPic(request):
    if request.user.user_profile:
        post = request.user.user_profile
        post.delete()
        return HttpResponseRedirect(reverse('app_login:profile'))