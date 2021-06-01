from rest_framework import serializers
from .models import Word


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'english', 'ukrainian', 'user']



class WordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['english', 'ukrainian', 'user']