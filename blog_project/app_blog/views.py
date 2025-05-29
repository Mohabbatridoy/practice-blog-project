from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment, Like
import uuid
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import CommentForm

# Create your views here.

class Blog_list(LoginRequiredMixin, ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = "blog_list.html"

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
    
@login_required
def BlogDetails(request, slug):
    blog = Blog.objects.get(slug=slug)
        
    comment_form = CommentForm()
    alredy_liked = Like.objects.filter(blog=blog, user=request.user)
    if alredy_liked:
        Liked = True
    else:
        Liked = False

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':slug}))

    return render(request, 'blog_details.html', context={'blog':blog, 'form':comment_form, 'liked':Liked})

@login_required
def Liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user

    already_liked = Like.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked = Like(blog=blog, user=user)
        liked.save()
    return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':blog.slug}))

@login_required
def Unliked(reqeust, pk):
    blog = Blog.objects.get(pk=pk)
    user = reqeust.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    if already_liked:
        already_liked.delete()
    return HttpResponseRedirect(reverse('app_blog:blog_details', kwargs={'slug':blog.slug}))



class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'my_blogs.html'

class UpdateBlog(LoginRequiredMixin, UpdateView):
    context_object_name = 'blog'
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'edit_blog.html'

    def get_success_url(self):
        return reverse_lazy('app_blog:blog_details', kwargs={'slug':self.object.slug})


