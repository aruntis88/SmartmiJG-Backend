from django.contrib import admin

from .models import *


admin.site.register(ProjectSegment)
admin.site.register(Project)
admin.site.register(Lead)
admin.site.register(Extension)
admin.site.register(Revision)
admin.site.register(Quote)
admin.site.register(QuotedProduct)

