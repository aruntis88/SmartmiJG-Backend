from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *


class ProductUnitViewSet(viewsets.ModelViewSet):
    """
    API view to list product units.
    """
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        msg, status, data = None, "failure", None
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid()
        if not valid:
            msg = serializer.errors
        else:
            self.perform_create(serializer)
            data = serializer.data
            msg = 'Product has been created successfully'
            status = "success"
        return Response({
            'data': data,
            'status': status,
            'message': msg,
        })

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to respond with a custom response.
        """
        msg, success = "", False

        instance = self.get_object()
        # self.perform_destroy(instance)
        try:
            self.perform_destroy(instance)
            msg = "Successfully Deleted"
            success = True
        except Exception as e:
            msg = str(e)

        return Response({'success': success, "message": msg})


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API view to list product categories.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 12
        if 'no_page' in self.request.query_params:
            paginator.page_size = self.queryset.count()

        queryset = self.queryset.model.query_objects.filter_by_query_params(
            request)
        queryset = queryset.order_by('-id')
        queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductCategorySerializer(queryset, many=True, context={
            'request': self.request})
        custom_data = {
            'data': serializer.data
        }
        return paginator.get_paginated_response(custom_data)

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to respond with a custom response.
        """
        msg, success = "", False

        instance = self.get_object()
        # self.perform_destroy(instance)
        try:
            self.perform_destroy(instance)
            msg = "Successfully Deleted"
            success = True
        except Exception as e:
            msg = str(e)

        return Response({'success': success, "message": msg})


class ProductViewSet(viewsets.ModelViewSet):
    """
    API view to list products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request).order_by('-id')
        return super(ProductViewSet, self).list(request)

    def create(self, request, *args, **kwargs):
        msg, status, data = None, "failure", None
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid()
        if not valid:
            msg = serializer.errors
        else:
            self.perform_create(serializer)
            data = serializer.data
            msg = 'Product has been created successfully'
            status = "success"
        return Response({
            'data': data,
            'status': status,
            'message': msg,
        })

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to respond with a custom response.
        """
        msg, success = "", False

        instance = self.get_object()
        # self.perform_destroy(instance)
        try:
            self.perform_destroy(instance)
            msg = "Successfully Deleted"
            success = True
        except Exception as e:
            msg = str(e)

        return Response({'success': success, "message": msg})


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    API view to list product variants.
    """
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request).order_by('-id')
        return super(ProductVariantViewSet, self).list(request)

    def create(self, request, *args, **kwargs):
        msg, success = None, False
        serializer = self.get_serializer(data=request.data, many=True)
        valid = serializer.is_valid()
        if not valid:
            msg = serializer.errors
        else:
            self.perform_create(serializer)
            msg = 'Successfully created'
            success = True
        return Response({
            'success': success,
            'msg': msg,
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to respond with a custom response.
        """
        msg, success = "", False

        instance = self.get_object()
        # self.perform_destroy(instance)
        try:
            self.perform_destroy(instance)
            msg = "Successfully Deleted"
            success = True
        except Exception as e:
            msg = str(e)

        return Response({'success': success, "message": msg})


class AvgCostRevisionViewSet(viewsets.ModelViewSet):
    """
    API view to list revisions.
    """
    queryset = AvgCostRevision.objects.all()
    serializer_class = AvgCostRevisionSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to respond with a custom response.
        """
        msg, success = "", False

        instance = self.get_object()
        # self.perform_destroy(instance)
        try:
            self.perform_destroy(instance)
            msg = "Successfully Deleted"
            success = True
        except Exception as e:
            msg = str(e)

        return Response({'success': success, "message": msg})


class FileUploadViewSet(viewsets.ModelViewSet):
    """
    API view to list revisions.
    """
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
