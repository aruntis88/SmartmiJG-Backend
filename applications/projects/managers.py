from django.db import models
from django.db.models import Q


class CustomProjectQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        company = request.GET.get('company', None)
        main_contractor = request.GET.get('main_contractor', None)
        main_sub_contractor = request.GET.get('main_sub_contractor', None)
        client = request.GET.get('client', None)
        q = request.GET.get('q', None)
        sort_by = request.GET.get('sort_by', None)
        str = request.GET.get('str', None)

        # filter
        if main_contractor:
            items = items.filter(main_contractor=main_contractor).distinct()
        if main_sub_contractor:
            items = items.filter(main_sub_contractor=main_sub_contractor).distinct()
        if client:
            items = items.filter(client=client).distinct()
        if company:
            items = items.filter(companies_linked__in=[company]).distinct()
        # sort
        if q == 'asc' and sort_by:
            items = items.order_by(sort_by).distinct()

        if q == 'des' and sort_by:
            items = items.order_by('-' + sort_by).distinct()

        if str:
            # str = str.strip().lower()
            items = items.filter(Q(reference_no__icontains=str) |
                                 Q(name__icontains=str)).distinct()
        return items


class LeadQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        q = request.GET.get('q', None)
        customer = request.GET.get('customer', None)
        assigned_to = request.GET.get('assigned_to', None)
        project = request.GET.get('project', None)
        received_by = request.GET.get('received_by', None)
        str = request.GET.get('str', None)

        if customer:
            items = items.filter(customer=customer).distinct()

        if assigned_to:
            items = items.filter(assigned_to=assigned_to).distinct()

        if received_by:
            items = items.filter(sales_engineer=received_by).distinct()

        if project:
            items = items.filter(project=project).distinct()

        if q == 'asc':
            items = items.order_by('due_date').distinct()

        if q == 'des':
            items = items.order_by('-due_date').distinct()

        if str:
            # str = str.strip().lower()
            items = items.filter(Q(reference_no__icontains=str) |
                                 Q(customer__name__icontains=str) |
                                 Q(project__name__icontains=str) |
                                 Q(company__name__icontains=str) |
                                 Q(contact_name__icontains=str) |
                                 Q(email__icontains=str) |
                                 Q(description__icontains=str) |
                                 Q(assigned_to__first_name__icontains=str) |
                                 Q(sales_engineer__first_name__icontains=str)).distinct()
        return items


class NoteQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        project = request.GET.get('project', None)
        quote = request.GET.get('quote', None)
        added_by = request.GET.get('added_by', None)
        customer = request.GET.get('customer', None)

        if project:
            items = items.filter(project=project).distinct()
        if customer:
            items = items.filter(customer=customer).distinct()
        if quote:
            items = items.filter(quote=quote).distinct()
        if added_by:
            items = items.filter(added_by=added_by).distinct()

        return items


class CustomQuoteQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        project = request.GET.get('project', None)
        customer = request.GET.get('customer', None)
        company = request.GET.get('company', None)
        engineer = request.GET.get('engineer', None)
        q = request.GET.get('q', None)
        sort_by = request.GET.get('sort_by', None)
        str = request.GET.get('str', None)

        if project:
            items = items.filter(project=project).distinct()
        if engineer:
            items = items.filter(lead__sales_engineer=engineer).distinct()
        if customer:
            items = items.filter(lead__customer=customer).distinct()
        if company:
            items = items.filter(company=company).distinct()
        # sort
        if q == 'asc' and sort_by:
            items = items.order_by(sort_by).distinct()

        if q == 'des' and sort_by:
            items = items.order_by('-' + sort_by).distinct()

        if str:
            # str = str.strip().lower()
            items = items.filter(Q(reference_no__icontains=str) |
                                 Q(erp_reference__icontains=str)).distinct()
        return items


class CustomHistoryQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        project = request.GET.get('project', None)
        customer = request.GET.get('customer', None)
        quote = request.GET.get('quote', None)

        if project:
            items = items.filter(project=project).distinct()
        if customer:
            items = items.filter(customer=customer).distinct()
        if quote:
            items = items.filter(quote=quote).distinct()

        return items
