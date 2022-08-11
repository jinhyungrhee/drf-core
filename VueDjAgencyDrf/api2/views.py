## ViewSet 사용
# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from .serializers import UserSerializer, PostSerializer, CommentSerializer
# from blog.models import Post, Comment

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer    

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer  
# =================================================================================
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from blog.models import Post, Comment
from .serializers import CommentSerializer, PostSerializer

class PostListAPIView(ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer

class PostRetrieveAPIView(RetrieveAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer

class CommentCreateAPIView(CreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer