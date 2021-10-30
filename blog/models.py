from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    count_view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({self.created_date})'


class Comment(models.Model):
    comment_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


