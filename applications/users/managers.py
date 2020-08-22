from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set'))
        # email = self.normalize_email(email)
        user = self.model(username=username, password=password, **extra_fields)
        user.save()
        user.set_password(user.password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class UserQueryset(models.QuerySet):
    """
    Custom QuerySet as manager provides filtering by GET parameters in the viewset.
    """

    def filter_by_query_params(self, request):
        """
        Provides filtering of QuerySet by GET parameters.
        """
        items = self
        designation = request.GET.get('designation', None)
        company = request.GET.get('company', None)
        role = request.GET.get('role', None)
        department = request.GET.get('department', None)
        q = request.GET.get('q', None)
        sort_by = request.GET.get('sort_by', None)

        if designation:
            items = items.filter(designation=designation).distinct()
        #sales engineers under a company
        if company:
            items = items.filter(company=company).distinct()
        if role:
            items = items.filter(role=role).distinct()
        if department:
            items = items.filter(department=department).distinct()

        if q == 'asc' and sort_by:
            items = items.order_by(sort_by).distinct()
        if q == 'des' and sort_by:
            items = items.order_by('-'+sort_by).distinct()

        return items
