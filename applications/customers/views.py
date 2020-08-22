from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Contact, Customer, CustomerType
from .serializers import CustomerSerializer, ContactSerializer, CustomerTypeSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    API view to list contacts.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def paginate_queryset(self, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        msg, success = None, False
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid()
        if not valid:
            msg = serializer.errors
        else:
            self.perform_create(serializer)
            msg = 'Contact has been created successfully'
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


class CustomerTypeViewSet(viewsets.ModelViewSet):
    """
    API view to list contacts.
    """
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer

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


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API view to list customers.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.model.query_objects.filter_by_query_params(
            request)
        return super(CustomerViewSet, self).list(request)

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