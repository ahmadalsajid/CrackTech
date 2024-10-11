from rest_framework import serializers
from .models import Tag, Question, FavoriteQuestion


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['created_at', 'updated_at']
        # fields = '__all__'
        # depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']

class FavoriteSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = FavoriteQuestion
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']