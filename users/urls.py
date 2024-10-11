from django.urls import path
from users.views import (
    DashboardViewSet,
)

urlpatterns = [
    path('Dashboard/', DashboardViewSet.as_view({
        'get': 'list',
    })),
]
