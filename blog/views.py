from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post, Comment, Hashtag, Category, Review
from blog.forms import PostForm, CommentForm, ReviewForm
from django.http import Http404
from django.db.models import Count, Avg
from django.core.exceptions import ObjectDoesNotExist


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
    avg_rang = post.reviews.aggregate(Avg('rang'))
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

    try:
        favorite = post.favorites.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        favorite = False

    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post_pk)
    reviews = Review.objects.filter(post=post_pk)

    return render(request, "blog/post_deteil.html", {'reviews': reviews, 'avg_rang':avg_rang['rang__avg'], 'post': post, 'comments': comments, 'comment_form': comment_form, 'favorites': favorite})


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
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
    cat_list = (Category.objects
                .annotate(Count('posts'))
                .filter(posts__count__gt=0)
                .order_by('-posts__count'))
    return render(request, 'blog/cat_list.html', {'cat_list': cat_list})


def post_list_cat(request, cat_pk):
    posts = Post.objects.filter(category=cat_pk, public=True)
    cat_list = (Category.objects
                .annotate(Count('posts'))
                .filter(posts__count__gt=0)
                .order_by('-posts__count'))

    cat = Category.objects.get(pk=cat_pk)
    return render(request, 'blog/post_list_cat.html', {'posts': posts, 'cat_list': cat_list, 'category': cat})


def change_favorite(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    try:
        favorite = post.favorites.get(pk=request.user.pk)
        post.favorites.remove(request.user)
    except ObjectDoesNotExist:
        post.favorites.add(request.user)
    post.save()
    lastpath = request.GET.get('lastpath', False)
    if lastpath:
        return redirect(lastpath)
    return redirect('post_detail', post_pk=post_pk)


def favorites_list(request):
    posts = Post.objects.filter(favorites=request.user.pk)
    return render(request, "blog/posts_list.html", {'posts': posts})


def post_review_add(request, post_pk):
    post = get_object_or_404(Post,pk=post_pk)
    post_reviews = post.reviews.filter(author__pk=request.user.pk).first()
    if request.method == "POST":
        if post_reviews:
            review_form = ReviewForm(request.POST, instance=post_reviews)
        else:
            review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.post = post
            review.save()
            return redirect('post_detail', post_pk=post_pk)
    else:
        if post_reviews:
            review_form = ReviewForm(instance=post_reviews)
        else:
            review_form = ReviewForm()

    return render(request, 'blog/review_post_add.html', {'form': review_form, 'post': post})
    #return redirect('post_detail', post_pk=post_pk)
