from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create/', views.post_create, name='post_create'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('signup/', views.signup, name='signup'),
    path('stories/<int:user_id>/', views.get_user_stories, name='get_user_stories'),
    path('story/create/', views.story_create, name='story_create'),
]