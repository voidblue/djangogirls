from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post


def post_list(request: HttpRequest):
    posts: list[Post] = Post.objects.order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request: HttpRequest, pk: int):
    post: Post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request: HttpRequest):
    if request.method == "POST":
        form: PostForm = PostForm(request.POST)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form: PostForm = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request: HttpRequest, pk: int):
    post: Post = Post.objects.get(pk=pk)
    if post is None:
        return redirect("404.html")

    if request.method == "POST":
        form: PostForm = PostForm(request.POST, instance=post)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form: PostForm = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form})

