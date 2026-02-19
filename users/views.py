from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django import forms

class EasySignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "" # Ism shartlarini ko'rsatmaslik

    def clean(self):
        cleaned_data = super().clean()
        # Djangoning inglizcha xatolarini ushlab, o'zbekchaga o'zgartiramiz
        for field in self.errors:
            for i, error in enumerate(self.errors[field]):
                if "too short" in error.lower():
                    self.errors[field][i] = "Parol juda qisqa (kamida 4 ta belgi bo'lsin)!"
                if "entirely numeric" in error.lower():
                    self.errors[field][i] = "Parol faqat raqamlardan iborat bo'lmasin!"
                if "common" in error.lower():
                    self.errors[field][i] = "Bu parol juda oddiy!"
        return cleaned_data

def post_list(request):
    posts = Post.objects.filter(status='global').order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def my_posts(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'my_posts.html', {'posts': posts})

def post_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status')
        Post.objects.create(author=request.user, title=title, content=content, status=status)
        return redirect('my_posts') 
    return render(request, 'post_form.html', {'title': 'Yangi post'})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Siz faqat o'z postingizni tahrirlay olasiz!")
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.status = request.POST.get('status')
        post.save()
        return redirect('my_posts')
    return render(request, 'post_form.html', {'post': post, 'title': 'Postni tahrirlash'})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Sizda o'chirish huquqi yo'q!")
    if request.method == "POST":
        post.delete()
        return redirect('my_posts')
    return render(request, 'post_confirm_delete.html', {'post': post})

def signup(request):
    if request.method == "POST":
        form = EasySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('post_list')
    else:
        form = EasySignupForm()
    return render(request, 'signup.html', {'form': form})