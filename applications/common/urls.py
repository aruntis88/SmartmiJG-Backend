from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register('companies', CompanyViewSet, basename='companies')
router.register('countries', CountryViewSet, basename='countries')
router.register('manufacturers', ManufacturerViewSet, basename='manufacturers')
# router.register('mfr/revisions', ManufacturerRevisionViewSet, basename='mfr-revisions')
router.register('terms', TermViewSet, basename='terms')

urlpatterns = [
    path('', include(router.urls)),
]
