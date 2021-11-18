from ..models import *
from rest_framework.views import APIView
from rest_framework.response import Response

# posts/views.py
from rest_framework import generics,permissions

from .serializers import *


class PostList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    
class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class ArticleCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self, serializer):
        categ = Category.objects.get(id = self.request.data['category'])
        serializer.save(category = categ, author=self.request.user)


class UnpublishedPosts(generics.ListAPIView):
    queryset = Article.objects.filter(status=0).order_by('-created_on')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    
class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)
        
        
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class PublishView(APIView):
    def patch(self, request, identifier, format=None):
        post = Article.objects.get(slug = identifier)
        post.status = 1
        post.save()
        serializer = ArticleSerializer(post)
        return Response(serializer.data)