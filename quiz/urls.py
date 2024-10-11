from django.urls import path
from quiz.views import (
    TagViewSet,
    QuestionViewSet
)


urlpatterns = [
    path('tags/', TagViewSet.as_view({
        'get': 'list',
    })),
    path('questions/', QuestionViewSet.as_view({
        'get': 'list',
    })),
]
