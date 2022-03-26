from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Hashtag(models.Model):
    tag = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.tag


class Category(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.title


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
    hashtags = models.ManyToManyField(Hashtag, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='posts')
    favorites = models.ManyToManyField(User, related_name='favorites_posts')

    def avg_rang(self):
        tmp = self.reviews.aggregate(Avg('rang'))
        return tmp['rang__avg']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # find hashtags in post text
        tmp = self.text
        for sep in '.!-,?':
            tmp = tmp.replace(sep, ' ')
        tags = [tag for tag in tmp.split() if tag.startswith('#') and len(tag) > 1]
        self.hashtags.clear()
        for tag in tags:
            obj, create = Hashtag.objects.get_or_create(tag=tag)
            self.hashtags.add(obj)

        # ob_tags = []
        # for tag in tags:
        #     obj, create = Hashtag.objects.get_or_create(tag=tag)
        #     ob_tags.append(obj)
        # self.hashtags.set(ob_tags)

    def html_hashtag(self):
        tags = self.hashtags.all()
        result = self.text
        for tag in tags:
            result = result.replace(tag.tag, f'<b class="hashtag">{tag.tag}</b>')
        result = result.replace('\n', '<br>')
        return result

    def __str__(self):
        return f'{self.title} ({self.created_date})'


class Comment(models.Model):
    comment_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rang = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
