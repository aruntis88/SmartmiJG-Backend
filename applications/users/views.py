from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API view to list services.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request)
        return super(UserViewSet, self).list(request)

    def create(self, request, *args, **kwargs):
        msg, success = None, False
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid()
        if not valid:
            msg = serializer.errors
        else:
            self.perform_create(serializer)
            msg = 'User has been created successfully'
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
