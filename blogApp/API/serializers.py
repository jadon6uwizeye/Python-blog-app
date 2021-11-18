from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Category
        
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = User
        

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many = False)
    author = UserSerializer(many = False)
    
    class Meta:
        fields = ('id', 'title','slug','category','author', 'content','status', 'picture','created_on', 'updated_on',)
        model = Article
        author = serializers.ReadOnlyField(source='author.username')

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment
        
    