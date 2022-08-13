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
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from blog.models import Post, Comment
from .serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer, PostLikeSerializer

class PostListAPIView(ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostListSerializer

class PostRetrieveAPIView(RetrieveAPIView):
  queryset = Post.objects.all()
  serializer_class = PostRetrieveSerializer

class CommentCreateAPIView(CreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

class PostLikeAPIView(UpdateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostLikeSerializer

  # update 메서드 오버라이딩
  def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 내부에 like + 1 로직 추가 (이후 serializer의 data변수에 dict 형태로 넣어줌)
        data = {'like' : instance.like + 1}
        # data = instance.like + 1
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # return Response(serializer.data)
        return Response(data['like'])
