from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='list'),
    path('new/', views.review_create, name='create'),
    path('<int:pk>/', views.review_detail, name='detail'),
    path('<int:pk>/edit/', views.review_update, name='update'),
    path('<int:pk>/delete/', views.review_delete, name='delete'),
]