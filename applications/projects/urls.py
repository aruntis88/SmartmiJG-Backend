from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register('segments', ProjectSegmentViewSet, basename='segments')
router.register('extensions', ExtensionViewSet, basename='extensions')
router.register('revisions', RevisionViewSet, basename='revisions')
router.register('listed', ProjectViewSet, basename='listed')
router.register('leads', LeadViewSet, basename='leads')
router.register('quotes', QuoteViewSet, basename='quotes')
router.register('quotedproducts', QuotedProductViewSet, basename='quotedproducts')
router.register('quotedvariants', QuotedProductVariantViewSet, basename='quotedvariants')
router.register('notes', NoteViewSet, basename='notes')
router.register('history', HistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
]
