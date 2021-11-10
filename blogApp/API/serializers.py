from rest_framework import serializers
from ..models import *


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title','slug','category','author', 'content', 'picture','created_on', 'updated_on',)
        model = Article
        author = serializers.ReadOnlyField(source='author.username')

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment