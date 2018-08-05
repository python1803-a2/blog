from math import ceil

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from post.helper import page_cache, page_count, get_top_n
from post.models import Post


def index(request):
    return HttpResponse("index")


def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, "create_post.html")
@page_count
@page_cache(5)
def read_post(request):
    post_id = int(request.GET.get("post_id"))
    # print(post_id)
    post = Post.objects.get(id=post_id)
    # print(post)
    return render(request, 'read_post.html', {"post": post})


def edit_post(request):
    if request.method == "POST":
        post_id = int(request.POST.get("post_id"))
        post = Post.objects.get(id=post_id)
        title = request.POST.get("title")
        content = request.POST.get("content")
        post.title = title
        post.content = content
        post.save()
        return redirect("/post/read/?post_id=%s" % post.id)
    else:
        post_id = int(request.GET.get("post_id"))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {"post": post})


def search_post(request):
    key_word = request.POST.get("keyword")
    posts = Post.objects.filter(content__contains=key_word)
    return render(request, 'search.html', {"posts": posts})

@page_cache(20)
def list_post(request):
    page = int(request.GET.get('page', 1))
    total = Post.objects.count()
    per_page = 10
    pages = ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    posts = Post.objects.all().order_by("-id")[start: end]
    return render(request, 'post_list.html', {"posts": posts, "pages": range(pages)})


def top(request):
    rank_data = get_top_n(10)
    print(rank_data)
    return render(request, 'top10.html', {'rank_data': rank_data})