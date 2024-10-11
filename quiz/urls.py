from django.urls import path
from quiz.views import (
    TagViewSet,
    QuestionViewSet,
    FavoriteViewSet,
    ReadViewSet,
)

urlpatterns = [
    path('tags/', TagViewSet.as_view({
        'get': 'list',
    })),
    path('questions/', QuestionViewSet.as_view({
        'get': 'list',
    })),
    path('favorites/', FavoriteViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('reads/', ReadViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
]
