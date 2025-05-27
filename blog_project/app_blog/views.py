from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Comment, Like
import uuid
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class Blog_list(LoginRequiredMixin, ListView):
    context_object_name = 'blog'
    model = Blog
    template_name = 'blog_list.html'

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = 'create_blog.html'

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ","-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))