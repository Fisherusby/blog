from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'public',
            'category',
            'title',
            'text',
            'image'
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            'comment_text'
        }


