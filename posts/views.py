from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer, serializers


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        request_data["created_by"] = request.user if request.user.is_authenticated else None
        serializer = PostSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass

    # def perform_create(self, serializer):
    #     if not hasattr(self.request.user, 'driver'):
    #         raise serializers.ValidationError('Only drivers can create posts.')
    #
    #     serializer.save(created_by=self.request.user.driver)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
