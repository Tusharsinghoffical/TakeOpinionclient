from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import BlogPost


def blog_list(request: HttpRequest) -> HttpResponse:
    posts = BlogPost.objects.all()
    return render(request, "blogs/list.html", {"posts": posts})


def blog_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blogs/detail.html", {"post": post})

# Create your views here.
