from django.urls import path
from .views import PostCreateView, PostDeleteView, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]