from django.db import models
from django.db.models import Manager

from applications.common.models import Country
from applications.customers.managers import CustomCustomerQueryset
from smartmibackend import settings
from smartmibackend.utils import phone_regex


class Contact(models.Model):
    name = models.CharField(max_length=30)
    # phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    designation = models.CharField(max_length=30)


class CustomerType(models.Model):
    type = models.CharField(max_length=30, unique=True)


class Customer(models.Model):
    TYPE_CHOICES = (
        ('MC', 'Main Contractor'),
        ('MS', 'Main Sub Contractor'),
        ('CT', 'Client'),
        ('DC', 'Design Consultant'),
        ('SC', 'Supervision Consultant'),
        ('TR', 'Trader'),
        ('SR', 'Subcontractor'),
        ('OT', 'Others')
    )
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='OT')
    customer_type = models.ManyToManyField(CustomerType, blank=True, related_name='customer_types')
    email = models.EmailField()
    fax = models.CharField(max_length=10, blank=True)
    # phone = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    address1 = models.TextField()
    address2 = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    website = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    introduced_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='introducers', on_delete=models.PROTECT)
    introduced_date = models.DateField()
    point_of_contact = models.ManyToManyField(Contact, related_name='contacts', blank=True)
    sales_engineers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sales_engineers')

    objects = Manager()
    query_objects = CustomCustomerQueryset.as_manager()

    class Meta:
        ordering = ['-id']
