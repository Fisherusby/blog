from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.http import Http404


def posts_list(request):
    posts = Post.objects.filter(public=True)
    return render(request, "blog/posts_list.html", {'posts': posts})


def posts_list_dr(request):
    posts = Post.objects.filter(public=False)
    for post in posts:
        post.hashtags_lst = post.hashtags.all()
    return render(request, "blog/posts_list.html", {'posts': posts})


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    else:
        post.count_view += 1
        post.save()
        post.hashtags_lst = post.hashtags.all()
       # post.html_text = post.html_hashtag

    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post_pk)

    return render(request, "blog/post_deteil.html", {'post': post, 'comments': comments, 'comment_form': comment_form})


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user
            post.save()
            post.find_hashtags()
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_add.html', {'form': form})


def del_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('posts_list')


def edit_post(request, post_pk):
    # post = get_object_or_404(Post, pk=post_pk)
    post = Post.objects.filter(pk=post_pk).first()
    if not post:
        raise Http404('Post not found')
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.find_hashtags()
            post.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.like += 1
    post.count_view -= 1
    post.save()
    return redirect('post_detail', post_pk=post_pk)


def post_dislike(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.dislike += 1
    post.count_view -= 1
    post.save()
    return redirect('post_detail', post_pk=post_pk)

