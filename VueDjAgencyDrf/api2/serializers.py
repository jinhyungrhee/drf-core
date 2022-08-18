from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Category, Tag
from blog.models import Post, Comment

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class PostListSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source='category.name')
    category = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['id', 'title', 'image', 'like', 'category']

class PostRetrieveSerializer(serializers.ModelSerializer):
    # 기존의 필드를 오버라이딩하여 사용
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['create_dt']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['id', 'title', 'image', 'like', 'category']

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like']

# 반복되는 속성들을 표현하는 Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

# 최종적으로 client에게 내려주는 값을 정의하는 Serializer
# 직접 필드를 정의할 때는 Serializer 클래스를 상속받아서 사용!

# 1. Nested Serializer
# class CateTagSerializer(serializers.Serializer):
#     cateList = CategorySerializer(many=True)
#     tagList = TagSerializer(many=True)

# 2. ListField() 사용
class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())

# =============== PostDetail =======================================
class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']

class CommentSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'update_dt']


# 일반 serializer 상속 -> 키(필드)를 직접 설정하는 경우
class PostSerializerDetail(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSerializerSub() # id와 title만 가져옴
    nextPost = PostSerializerSub() # id와 title만 가져옴
    commentList = CommentSerializerSub(many=True) # 일부 필드만 사용하는 serializer('id', 'content', 'update_dt')


