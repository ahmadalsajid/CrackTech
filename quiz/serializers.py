from rest_framework import serializers
from .models import Tag, Question, FavoriteQuestion, ReadQuestion
from icecream import ic


class NestedTagSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()
    user_total_favorites = serializers.SerializerMethodField()
    user_total_reads = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        exclude = ['created_at', 'updated_at']

    def to_representation(self, instance):
        self.fields['tags'] = NestedTagSerializer(many=True, read_only=True)
        return super(NestedTagSerializer, self).to_representation(instance)

    def get_total_questions(self, obj):
        return obj.questions.count()

    def get_user_total_favorites(self, obj):
        _count = 0
        try:
            _questions = obj.questions.values_list('id', flat=True)
            _count = FavoriteQuestion.objects.filter(questions__in=_questions).distinct().count()
            # _count = FavoriteQuestion.objects.filter(questions__in=_questions).count()
        except Exception as e:
            ic(e)
        return _count

    def get_user_total_reads(self, obj):
        _count = 0
        try:
            _questions = obj.questions.values_list('id', flat=True)
            _count = ReadQuestion.objects.filter(questions__in=_questions).distinct().count()
            # _count = ReadQuestion.objects.filter(questions__in=_questions).count()
        except Exception as e:
            ic(e)
        return _count


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['created_at', 'updated_at']
        # fields = '__all__'
        # depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = FavoriteQuestion
        exclude = ['created_at', 'updated_at']
