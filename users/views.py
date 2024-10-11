from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from icecream import ic
from users.serializers import LoginViewSerializer
from users.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'


class LoginView(TokenObtainPairView):
    serializer_class = LoginViewSerializer


class DashboardViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    @method_decorator(cache_page(60 * 15))  # ( second x minute)
    @method_decorator(vary_on_cookie)
    def list(self, request):
        pass
