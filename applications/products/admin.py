from django.contrib import admin

from .models import *

admin.site.register(ProductCategory)
admin.site.register(ProductUnit)
admin.site.register(Product)
admin.site.register(ProductVariant)