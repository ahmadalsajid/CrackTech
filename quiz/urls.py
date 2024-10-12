from django.urls import path
from quiz.views import (
    TagViewSet,
    TagSummaryViewSet,
    QuestionViewSet,
    FavoriteViewSet,
    ReadViewSet,
)

urlpatterns = [
    path('tags/', TagViewSet.as_view({
        'get': 'list',
    })),
    path('tags-summary/', TagSummaryViewSet.as_view({
        'get': 'list',
    })),
    path('questions/', QuestionViewSet.as_view({
        'get': 'list',
    })),
    path('favorites/', FavoriteViewSet.as_view({
        'get': 'list',
    })),
    path('favorites/<int:pk>/', FavoriteViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    })),
    path('reads/', ReadViewSet.as_view({
        'get': 'list',
    })),
    path('reads/<int:pk>/', ReadViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    })),
]
