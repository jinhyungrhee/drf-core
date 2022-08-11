# from django.urls import path, include
# from rest_framework import routers
# from .views import UserViewSet, PostViewSet, CommentViewSet

# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet)

# urlpatterns = [
#     path('', include(router.urls)),

# ]

from django.urls import path
from . import views

urlpatterns = [
  path('post/', views.PostListAPIView.as_view(), name='post-list'),
  path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),
  path('comment/', views.CommentCreateAPIView.as_view(), name='comment-create'),
]