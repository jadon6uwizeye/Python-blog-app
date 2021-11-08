from ..models import *

# posts/views.py
from rest_framework import generics

from .serializers import *


class PostList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer