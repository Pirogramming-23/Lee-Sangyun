from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='list'),
    path('new/', views.ReviewCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete'),
]
