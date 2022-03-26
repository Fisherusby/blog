from django.urls import path
from blog.api import api_views

urlpatterns = [
    path('category', api_views.CategoryList.as_view()),
    path('category/<int:pk>', api_views.CategoryDetail.as_view()),
    path('post', api_views.PostList.as_view()),
    path('post/<int:pk>', api_views.PostDetail.as_view()),
]
