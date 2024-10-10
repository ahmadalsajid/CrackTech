from django.urls import path
from quiz.views import (
    TagViewSet
)


urlpatterns = [
    path('tags/', TagViewSet.as_view({
        'get': 'list',
        # 'post': 'create'
    })),
]
