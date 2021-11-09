from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('list_dr', views.posts_list_dr, name='posts_list_dr'),
    path('post_detail/<int:post_pk>', views.post_detail, name='post_detail'),
    path('add_post', views.add_post, name='add_post'),
    path('del_post/<int:post_pk>', views.del_post, name='del_post'),
    path('edit_post/<int:post_pk>', views.edit_post, name='edit_post'),
    path('post_like/<int:post_pk>', views.post_like, name='post_like'),
    path('post_dislike/<int:post_pk>', views.post_dislike, name='post_dislike'),
    path('hashtag/<str:ht_tag>', views.post_list_tag, name='post_list_tag'),
    path('hashtag_list', views.hashtag_list, name='hashtag_list'),
    path('category_list', views.category_list, name='category_list'),
    path('category/<int:cat_pk>', views.post_list_cat, name='post_list_cat'),
    path('change_favorite/<int:post_pk>', views.change_favorite, name='change_favorite'),
    path('favorites_list', views.favorites_list, name='favorites_list')
]

