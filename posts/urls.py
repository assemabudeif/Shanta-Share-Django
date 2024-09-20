from django.urls import path
from .views import PostCreateView, PostListView, PostDetailsView, calculate_delivery_fees_view, \
    DriverPostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('details/<int:pk>', PostDetailView.as_view(), name='post-post-details'),
    path('driver-posts/', DriverPostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailsView.as_view(), name='post-details'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    # path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('calculate_fees/', calculate_delivery_fees_view, name='calculate-fees'),

]
