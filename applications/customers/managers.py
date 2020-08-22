from django.db import models
from django.db.models import Q


class CustomCustomerQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        type = request.GET.get('type', None)
        country = request.GET.get('country', None)
        active = request.GET.get('active', None)
        q = request.GET.get('q', None)
        sort_by = request.GET.get('sort_by', None)
        str = request.GET.get('str', None)

        if type:
            items = items.filter(customer_type__id__in=[type]).distinct()
        if country:
            items = items.filter(country=country).distinct()
        if active:
            items = items.filter(is_active=active).distinct()
        if q == 'asc' and sort_by:
            items = items.order_by(sort_by).distinct()
        if q == 'des' and sort_by:
            items = items.order_by('-'+sort_by).distinct()
        if str:
            # str = str.strip().lower()
            items = items.filter(Q(name__icontains=str) |
                                 Q(email__icontains=str)).distinct()

        return items
