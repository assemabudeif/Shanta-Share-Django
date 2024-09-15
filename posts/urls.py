from django.urls import path
from .views import PostCreateView, PostDeleteView, PostListView, PostDetailsView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailsView.as_view(), name='post-details'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]