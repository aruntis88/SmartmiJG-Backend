from django.db import models
from django.db.models import Q


class CustomProductVariantQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        pdt = request.GET.get('pdt', None)

        if pdt:
            items = items.filter(product=pdt).distinct()

        project = request.GET.get('project', None)
        q = request.GET.get('q', None)

        # Product of product varaiant in QuotedProduct of Quote of Lead with project

        if project:
            items = items.filter(quotedproduct__quote__lead__project=project).distinct()

        if q == "unquoted":
            items = items.exclude(quotedproduct__quote__lead__project=project).distinct()

        return items


class CustomProductQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        project = request.GET.get('project', None)
        category = request.GET.get('category', None)
        company = request.GET.get('company', None)
        manufacturer = request.GET.get('manufacturer', None)
        is_active = request.GET.get('is_active', None)
        q = request.GET.get('q', None)
        str = request.GET.get('str', None)

# Product of product varaiant in QuotedProduct of Quote of Lead with project

        if project:
            items = items.filter(productvariant__quotedproduct__quote__lead__project=project).distinct()

        if category:
            items = items.filter(category=category).distinct()

        if company:
            items = items.filter(company=company).distinct()

        if manufacturer:
            items = items.filter(manufacturer=manufacturer).distinct()

        if is_active:
            items = items.filter(is_active=is_active).distinct()

        if q == "unquoted":
            items = items.exclude(productvariant__quotedproduct__quote__lead__project=project).distinct()

        if str:
            # str = str.strip().lower()
            items = items.filter(Q(name__icontains=str)).distinct()
        return items


class CustomProductCategoryQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        company = request.GET.get('company', None)

        if company:
            items = items.filter(company=company).distinct()

        return items
