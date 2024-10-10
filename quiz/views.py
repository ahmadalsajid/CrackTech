from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework import status
from icecream import ic
from quiz.serializers import TagSerializer
from quiz.models import Tag
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'


class TagViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

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
