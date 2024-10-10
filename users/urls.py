from django.urls import path
from users.views import (
    StudentViewSet,
)

urlpatterns = [
    path('students/', StudentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('students/<int:pk>/', StudentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]
