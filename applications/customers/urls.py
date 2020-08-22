from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register('accounts', CustomerViewSet, basename='accounts')
router.register('contacts', ContactViewSet, basename='contacts')
router.register('types', CustomerTypeViewSet, basename='types')

urlpatterns = [
    path('', include(router.urls)),
]
