from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from icecream import ic
from quiz.serializers import TagSerializer, QuestionSerializer, NestedTagSerializer
from quiz.models import Tag, Question, FavoriteQuestion, ReadQuestion
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page
from users.views import CustomPagination
from django.db import connection, reset_queries


class TagSummaryViewSet(viewsets.ViewSet):
    # pagination_class = CustomPagination

    @extend_schema(
        description='Get tags and associated summary',
        responses=NestedTagSerializer(many=True),
    )
    # @method_decorator(cache_page(60 * 15))  # ( second x minute)
    # @method_decorator(vary_on_cookie)
    def list(self, request):
        _tag_id = request.query_params.get('tag_id', None)
        if _tag_id:
            queryset = Tag.objects.filter(id=_tag_id).select_related('parent')
        else:
            queryset = Tag.objects.filter(parent=None)
        _s = NestedTagSerializer(queryset, many=True)
        return Response(_s.data, status=status.HTTP_200_OK)


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


class FavoriteViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @extend_schema(
        description='Get favorite questions',
        responses=QuestionSerializer(many=True),
    )
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

    @extend_schema(
        description='Mark question(s) as favorite',
        responses=QuestionSerializer(many=True),
    )
    def create(self, request, pk=None):  # pk = id of Question
        _user = request.user
        try:
            if FavoriteQuestion.objects.filter(user=_user).exists():
                # the user already has favorites, just update it
                _user.favorite.questions.add(pk)
            else:
                # the user is marking for the first time, create one for now
                FavoriteQuestion.objects.create(user=_user)
                _user.favorite.questions.add(pk)

            paginator = self.pagination_class()
            queryset = _user.favorite.questions.all()
            result_page = paginator.paginate_queryset(queryset, request)
            _serialize = QuestionSerializer(result_page, many=True)
            return paginator.get_paginated_response(_serialize.data)
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):  # pk = id of Question
        _user = request.user
        try:
            if FavoriteQuestion.objects.filter(user=_user).exists():
                # the user already has favorites, just update it
                _user.favorite.questions.remove(pk)
            else:
                # the user does not fave any favorite, so delete is not allowed
                raise Exception('The user has no favorite questions')

            return Response(
                {
                    'detail': 'Removed question from favorite',
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class ReadViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='status',
                             description='Filter by Question read or unread',
                             required=False,
                             type=str,
                             enum=['read', 'unread']),
        ],
        description='Get read questions',
        responses=QuestionSerializer(many=True),
    )
    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        _user = request.user
        _read_status = request.GET.get('status', 'read')  # choices = [read, unread]
        try:
            paginator = self.pagination_class()
            if _read_status.lower() == 'unread':
                _excluded_questions = list(_user.read.questions.values_list('id', flat=True)) if _user.read else []
                queryset = Question.objects.exclude(id__in=_excluded_questions)
            else:
                queryset = _user.read.questions.all()
            result_page = paginator.paginate_queryset(queryset, request)
            _serialize = QuestionSerializer(result_page, many=True)
            return paginator.get_paginated_response(_serialize.data)
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description='Mark question(s) as Read',
        responses=QuestionSerializer(many=True),
    )
    def create(self, request, pk=None):  # pk = id of Question
        _user = request.user
        try:
            if ReadQuestion.objects.filter(user=_user).exists():
                # the user already has favorites, just update it
                _user.read.questions.add(pk)
            else:
                # the user is marking for the first time, create one for now
                ReadQuestion.objects.create(user=_user)
                _user.read.questions.add(pk)

            paginator = self.pagination_class()
            queryset = _user.favorite.questions.all()
            result_page = paginator.paginate_queryset(queryset, request)
            _serialize = QuestionSerializer(result_page, many=True)
            return paginator.get_paginated_response(_serialize.data)
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):  # pk = id of Question
        _user = request.user
        try:
            if ReadQuestion.objects.filter(user=_user).exists():
                # the user already has favorites, just update it
                _user.read.questions.remove(pk)
            else:
                # the user does not fave any favorite, so delete is not allowed
                raise Exception('The user has no read questions')

            return Response(
                {
                    'detail': 'Removed question from read',
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            ic(e)
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
