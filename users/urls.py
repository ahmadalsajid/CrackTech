from django.urls import path
from users.views import (
    DashboardViewSet,
)

urlpatterns = [
    path('dashboard/', DashboardViewSet.as_view({
        'get': 'list',
    })),
]
