from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register('accounts', UserViewSet, basename='accounts')

urlpatterns = [
    path('users/', include(router.urls)),
]
