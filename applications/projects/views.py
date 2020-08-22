from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import *
from .serializers import *


class ProjectSegmentViewSet(viewsets.ModelViewSet):
    """
    API view to list project segments.
    """
    queryset = ProjectSegment.objects.all()
    serializer_class = ProjectSegmentSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)


class ExtensionViewSet(viewsets.ModelViewSet):
    """
    API view to list extensions.
    """
    queryset = Extension.objects.all()
    serializer_class = ExtensionSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)


class RevisionViewSet(viewsets.ModelViewSet):
    """
    API view to list revisions.
    """
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer

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


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API view to list projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request)
        return super(ProjectViewSet, self).list(request)

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


class LeadViewSet(viewsets.ModelViewSet):
    """
    API view to list leads.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request)
        return super(LeadViewSet, self).list(request)

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


class QuoteViewSet(viewsets.ModelViewSet):
    """
    API view to list lead sources.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request)
        return super(QuoteViewSet, self).list(request)

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


class QuotedProductViewSet(viewsets.ModelViewSet):
    """
    API view to list quoted products.
    """
    queryset = QuotedProduct.objects.all()
    serializer_class = QuotedProductSerializer

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


class QuotedProductVariantViewSet(viewsets.ModelViewSet):
    """
    API view to list quoted products.
    """
    queryset = QuotedProductVariant.objects.all()
    serializer_class = QuotedProductVariantSerializer

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


class NoteViewSet(viewsets.ModelViewSet):
    """
    API view to list quoted products.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request).order_by('-id')
        return super(NoteViewSet, self).list(request)

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


class HistoryViewSet(viewsets.ModelViewSet):
    """
    API view to list quoted products.
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request).order_by('-id')
        return super(HistoryViewSet, self).list(request)

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
