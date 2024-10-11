from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework import status
from icecream import ic
from quiz.serializers import TagSerializer, QuestionSerializer, FavoriteSerializer
from quiz.models import Tag, Question, FavoriteQuestion
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page
from users.views import CustomPagination
from django.db import connection, reset_queries


class TagViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))  # ( second x minute)
    @method_decorator(vary_on_cookie)
    def list(self, request):
        queryset = Tag.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        _serialize = TagSerializer(result_page, many=True)
        # return Response(_serialize.data, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(_serialize.data)

    def retrieve(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class QuestionViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))  # ( second x minute)
    @method_decorator(vary_on_cookie)
    def list(self, request):
        queryset = Question.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        _serialize = QuestionSerializer(result_page, many=True)
        # return Response(_serialize.data, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(_serialize.data)

    def retrieve(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class FavoriteViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        reset_queries()
        _user = request.user
        try:
            paginator = self.pagination_class()
            queryset = _user.favorite.questions.all()
            result_page = paginator.paginate_queryset(queryset, request)
            _serialize = QuestionSerializer(result_page, many=True)
            # return Response(_serialize.data, status=status.HTTP_200_OK)
            ic(connection.queries)
            ic(len(connection.queries))
            return paginator.get_paginated_response(_serialize.data)
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class ReadViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        reset_queries()
        _user = request.user
        try:
            paginator = self.pagination_class()
            queryset = _user.read.questions.all()
            result_page = paginator.paginate_queryset(queryset, request)
            _serialize = QuestionSerializer(result_page, many=True)
            # return Response(_serialize.data, status=status.HTTP_200_OK)
            ic(connection.queries)
            ic(len(connection.queries))
            return paginator.get_paginated_response(_serialize.data)
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
