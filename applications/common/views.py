from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import *
from .serializers import *


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API view to list companies.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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


class CountryViewSet(viewsets.ModelViewSet):
    """
    API view to list countries.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

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


# class ManufacturerRevisionViewSet(viewsets.ModelViewSet):
#     """
#     API view to list manufacturers.
#     """
#     queryset = ManufacturerRevision.objects.all()
#     serializer_class = ManufacturerRevisionSerializer

#     def paginate_queryset(self, *args, **kwargs):
#         if 'no_page' in self.request.query_params:
#             return None
#         return super().paginate_queryset(*args, **kwargs)


#     def destroy(self, request, *args, **kwargs):
#         """
#         Custom destroy method to respond with a custom response.
#         """
#         msg, success = "", False

#         instance = self.get_object()
#         # self.perform_destroy(instance)
#         try:
#             self.perform_destroy(instance)
#             msg = "Successfully Deleted"
#             success = True
#         except Exception as e:
#             msg = str(e)

#         return Response({'success': success, "message": msg})


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    API view to list manufacturers.
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

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


class TermViewSet(viewsets.ModelViewSet):
    """
    API view to list manufacturers.
    """
    queryset = Term.objects.all()
    serializer_class = TermSerializer

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