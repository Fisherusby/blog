from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post, Comment, Hashtag, Category
from blog.forms import PostForm, CommentForm
from django.http import Http404
from django.db.models import Count


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
        # post.hashtags_lst = post.hashtags.all()
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


def post_list_tag(request, ht_tag):
    posts = Post.objects.filter(hashtags__tag=ht_tag, public=True)
    hashtags = (Hashtag.objects
                .values('tag')
                .annotate(tag_count=Count('posts'))
                .filter(tag_count__gt=0)
                .order_by('-tag_count')
                )
    hashtag = Hashtag.objects.get(tag=ht_tag)
    return render(request, 'blog/post_list_tag.html', {'posts': posts, 'hashtags': hashtags, 'hashtag': hashtag})


def hashtag_list(request):
    # SELECT tag, COUNT(posts) AS tag_count FROM Hashtag GROUP BY tag ORDER BY tag_count DESC
    hashtags = (Hashtag.objects
                .values('tag')
                .annotate(tag_count=Count('posts'))
                .filter(tag_count__gt=0)
                .order_by('-tag_count')
                )
    return render(request, 'blog/hashtag_list.html', {'hashtags': hashtags})


def category_list(request):
    cat_list = Category.objects.all()
    return render(request, 'blog/cat_list.html', {'cat_list': cat_list})

def post_list_cat(request, cat_pk):
    posts = Post.objects.filter(category=cat_pk, public=True)
    cat_list = Category.objects.all().annotate(Count('posts')).filter(posts__count__gt=0).order_by('-posts__count')
    cat = Category.objects.get(pk=cat_pk)
    return render(request, 'blog/post_list_cat.html', {'posts': posts, 'cat_list': cat_list, 'category': cat})

