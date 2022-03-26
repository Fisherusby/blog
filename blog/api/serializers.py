from rest_framework import serializers
from django.contrib.auth.models import User

from blog.models import Post, Comment, Hashtag, Review, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'description'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'comment_text',
            'created_date',
            'author',
        )


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = (
            'id',
            'tag',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
        )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'image',
            'text',
            'created_date',
            'author',
            'count_view',
            'like',
            'dislike',
            'public',
            'hashtags',
            'category',
            'comments',
            'reviews',
        ]

