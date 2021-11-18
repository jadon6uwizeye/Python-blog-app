from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Category
        
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('username','first_name','last_name','email')
        model = User
        

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many = False, read_only=True)
    author = UserSerializer(many = False, read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        fields = ('id', 'title','slug','category','author', 'content','status', 'picture','created_on', 'updated_on',)
        model = Article

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment
        
    