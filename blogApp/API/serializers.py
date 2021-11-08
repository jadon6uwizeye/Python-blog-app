from rest_framework import serializers
from ..models import *


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title','slug', 'content', 'picture','created_on', 'updated_on',)
        model = Article