from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, View, TemplateView
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin

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



class UserProfileDetails(LoginRequiredMixin, DetailView):
    context_object_name = 'user'
    model = User
    template_name = 'Profile.html'