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
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.models import Post, Comment, Category, Tag
from .serializers import CateTagSerializer, CommentSerializer, PostListSerializer, PostRetrieveSerializer, PostLikeSerializer, PostSerializerDetail
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

# class PostListAPIView(ListAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostListSerializer

# class PostRetrieveAPIView(RetrieveAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostRetrieveSerializer

class CommentCreateAPIView(CreateAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

# class PostLikeAPIView(UpdateAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostLikeSerializer

#   # PATCH method
#   # update 메서드 오버라이딩
#   def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         # 내부에 like + 1 로직 추가 (이후 serializer의 data변수에 dict 형태로 넣어줌)
#         data = {'like' : instance.like + 1}
#         # data = instance.like + 1
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         # return Response(serializer.data)
#         return Response(data['like'])

class PostLikeAPIView(GenericAPIView):
  queryset = Post.objects.all()
  # serializer_class = PostLikeSerializer

  # GET method (역직렬화 과정 불필요)**
  def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()

        return Response(instance.like)

# Category와 Tag 두 테이블 모두를 가져와서 사용 -> APIView 또는 GenericAPIView 사용!
# Generic View들은 모두 하나의 테이블을 대상으로 처리하는 View**
class CateTagAPIView(APIView):
  # 직렬화(serialize) 방향: 테이블 -> serialize -> response
  def get(self, request, *args, **kwargs):
    # 1. 테이블
    cateList = Category.objects.all()
    tagList = Tag.objects.all()
    # 1-1. serializer에 넘겨줄 data 구성(중요: key와 필드명 일치!)**
    data = {
      'cateList' : cateList,
      'tagList' : tagList,
    }
    # 2. serialize
    serializer = CateTagSerializer(instance=data)
    # 3. response
    return Response(serializer.data)

# pagination overriding
class PostPageNumberPagination(PageNumberPagination):
    page_size = 3 # 한 페이지 당 항목 개수
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))

class PostListAPIView(ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostListSerializer
  pagination_class = PostPageNumberPagination

  def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }

# exception 처리 함수
def get_prev_next(instance):
  try:
    prev = instance.get_previous_by_update_dt()
  except instance.DoesNotExist:
    prev = None

  try:
    next_ = instance.get_next_by_update_dt()
  except instance.DoesNotExit:
    next_ = None

  return prev, next_

class PostRetrieveAPIView(RetrieveAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializerDetail

  def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # prevInstance = instance.get_previous_by_update_dt() # update_dt를 기준으로 앞에 있는 인스턴스를 가져오는 메서드(built-in)
        # nextInstance = instance.get_next_by_update_dt() # update_dt를 기준으로 뒤에 있는 인스턴스를 가져오는 메서드
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all() # 현재 post에 달려있는 comment 전부 가져오는 ORM 쿼리문
        data = {
          'post' : instance,
          'prevPost' : prevInstance,
          'nextPost' : nextInstance,
          'commentList' : commentList,
        }
        serializer = self.get_serializer(instance=data) # 테이블에서 가져온 데이터를 serializer에 공급
        return Response(serializer.data) # serializer.data 에서 '직렬화' 과정이 이루어짐! **

  def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }