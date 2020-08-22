from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd

from applications.common.models import Company, Manufacturer, Country
from applications.products.managers import *
from smartmibackend import settings


class ProductCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    legendLabel = models.CharField(max_length=60, blank=True, null=True)
    legendValue = models.CharField(max_length=60, blank=True, null=True)
    tooltip = models.CharField(max_length=60, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True) # mandatory

    objects = Manager()
    query_objects = CustomProductCategoryQueryset.as_manager()


class ProductUnit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=30, unique=True)

    class Meta:
        unique_together = ['name', 'symbol']


class AvgCostRevision(models.Model):
    revision_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="avg_cost_revision_by")
    revision_date = models.DateTimeField(blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='products/',  default='img/users/no-img.jpg', blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT) # mandatory
    company = models.ForeignKey(Company, on_delete=models.PROTECT) # mandatory
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT) # mandatory
    is_active = models.BooleanField(default=True)
    to_append = models.BooleanField(default=False)
    sales_engineers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ['name']

    objects = Manager()
    query_objects = CustomProductQueryset.as_manager()


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True)
    product_code = models.CharField(max_length=25) #part_co
    manufacturer_part_code = models.CharField(max_length=25, blank=True) # optional
    unit = models.ForeignKey(ProductUnit, on_delete=models.PROTECT) #unit name
    runit_price = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True) #unit cost
    average_cost = models.DecimalField(max_digits=20, decimal_places=3)
    old_average_cost = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    min_sales_price = models.DecimalField(max_digits=20, decimal_places=3)
    origin_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    note = models.TextField(blank=True)
    avg_cost_revisions = models.ManyToManyField(AvgCostRevision, related_name="avg_cost_revisions", blank=True)

    objects = Manager()
    query_objects = CustomProductVariantQueryset.as_manager()


class FileUpload(models.Model):
    FILE_TYPES = (
        ('PA', 'PA'),
        ('PV', 'PV'),
    )
    file = models.FileField(upload_to='products/')
    type = models.CharField(max_length=2, choices=FILE_TYPES, default='PA')


@receiver(post_save, sender=FileUpload)
def bulk_upload(sender, instance=None, created=False, **kwargs):
    if instance.type == 'PA':
        data = pd.read_excel(instance.file, header=1)
        for index, row in data.iterrows():
            ProductVariant.objects.filter(product_code=row[1]).update(old_average_cost=row[2], average_cost=row[3])
    if instance.type == 'PV':
        data = pd.read_excel(instance.file, header=1)
        for index, row in data.iterrows():
            try:
                unit = ProductUnit.objects.filter(symbol=row[4])[0]
            except:
                unit = ProductUnit.objects.create(name="Unit-" + str(row[4]), symbol=row[4])[0]
            try:
                country = Country.objects.filter(name=row[5])[0]
            except:
                country = Country.objects.create(name=row[5])
            try:
                pdt = Product.objects.filter(name=row[7])[0]
            except:
                pdt = Product.objects.latest('id')
            ProductVariant.objects.create(product=pdt, description= row[6], product_code=row[0], origin_country=country,
                                 unit=unit, min_sales_price=row[3], average_cost=row[2], manufacturer_part_code=row[1])

    instance.delete()

