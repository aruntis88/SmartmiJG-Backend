from django.db import models

from smartmibackend import settings
from smartmibackend.utils import phone_regex


class Country(models.Model):
    name = models.CharField(max_length=100)


class Company(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='company/logos/', default='img/users/no-img.jpg', null=True)
    code = models.CharField(max_length=25)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)
    # phone = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)
    website = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField(default=True)  # status
    enable_reports = models.BooleanField(default=True)  # status
    is_group = models.BooleanField(default=False)
    color = models.CharField(max_length=25, blank=True, null=True)
    header_img = models.ImageField(upload_to='company/headers/', default='img/users/no-img.jpg', null=True)
    footer_img = models.ImageField(upload_to='company/footers/', default='img/users/no-img.jpg', null=True)

    class Meta:
        unique_together = ['name']


# class ManufacturerRevision(models.Model):
#     revision_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mfr_revision_by")
#     revision_date = models.DateTimeField(blank=True, null=True)
#     revised_cost = models.DecimalField(max_digits=20, decimal_places=3)


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)
    website = models.CharField(max_length=60, blank=True)
    logo = models.ImageField(upload_to='manufacturer/logos/', default='img/users/no-img.jpg', null=True)
    mfr_part_code = models.CharField(max_length=25, blank=True)
    # mfr_average_cost = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    # # mfr_revisions = models.ManyToManyField(ManufacturerRevision, related_name="mfr_revisions", blank=True)
    # start_date = models.DateTimeField(blank=True, null=True)
    # end_date = models.DateTimeField(blank=True, null=True)
    # updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mfr_updated_by",
    #                                blank=True, null=True)
    # company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mfr_company",
    #                             blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Term(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
