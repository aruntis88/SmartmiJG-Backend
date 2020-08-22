from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register('units', ProductUnitViewSet, basename='units')
router.register('categories', ProductCategoryViewSet, basename='categories')
router.register('list', ProductViewSet, basename='list')
router.register('variants', ProductVariantViewSet, basename='variants')
router.register('avgrevisions', AvgCostRevisionViewSet, basename='avgrevisions')
router.register('files', FileUploadViewSet, basename='files')

urlpatterns = [
    path('', include(router.urls)),
]
