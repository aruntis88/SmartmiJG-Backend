from django.db import models
from django.db.models import Manager
import django

from applications.common.models import Country, Company, Term
from applications.customers.models import Customer
from applications.products.models import Product, ProductVariant, ProductCategory
from applications.projects.managers import *
from smartmibackend import settings


class ProjectSegment(models.Model):
    name = models.CharField(max_length=60)


class Project(models.Model):
    STAGES = (
        ('T', 'Tender'),
        ('J', 'Job In Hand'),
    )
    STATUS = (
        ('TR', 'Tender'),
        ('JC', 'JIH-Main Contractor'),
        ('J1', 'JIH-Stage 1'),
        ('J2', 'JIH-Stage 2'),
        ('J3', 'JIH-Stage 3'),
        ('J4', 'JIH-Stage 4'),
        ('CL', 'Closed'),
        ('CA', 'Cancelled')
    )

    reference_no = models.CharField(max_length=60, blank=True)
    name = models.CharField(max_length=60)
    stage = models.CharField(max_length=1, choices=STAGES, default='T')
    status = models.CharField(max_length=2, choices=STATUS, default='TR')
    segment = models.ForeignKey(ProjectSegment, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=20, decimal_places=3)
    location = models.TextField(blank=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    companies_linked = models.ManyToManyField(Company, blank=True)
    intro_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    intro_date = models.DateField()
    completion = models.DecimalField(max_digits=20, decimal_places=3, blank=True)
    exp_start_date = models.DateField(blank=True, null=True)
    exp_end_date = models.DateField(blank=True, null=True)
    main_contractor = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='main_contractors', blank=True, null=True)
    main_sub_contractor = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sub_contractors', blank=True, null=True)
    client = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='clients', blank=True, null=True)
    design_consultant = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='design_consultants', blank=True, null=True)
    supervision_consultant = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='supervision_consultants', blank=True, null=True)

    objects = Manager()
    query_objects = CustomProjectQueryset.as_manager()

    class Meta:
        ordering = ['-id']


class Lead(models.Model):
    SOURCES = (
        ('P', 'Phone'),
        ('F', 'Fax'),
        ('W', 'Website'),
        ('V', 'Visit'),
        ('E', 'Email'),
        ('O', 'Others'),
    )
    reference_no = models.CharField(max_length=25, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="lead_project")
    lead_source = models.CharField(max_length=2, choices=SOURCES, default='O')
    sales_engineer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="engineer_lead")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assigned_to_lead")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="lead_company", blank=True, null=True) # company name is required to generate lead id
    due_date = models.DateField(blank=True, null=True)
    contact_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    description = models.ManyToManyField(ProductCategory, blank=True)

    objects = Manager()
    query_objects = LeadQueryset.as_manager()

    class Meta:
        ordering = ['-id']


class Revision(models.Model):
    # quote = models.ForeignKey(Quote, on_delete=models.PROTECT, related_name="quote_revisions")
    revision_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="revision_by")
    revision_date = models.DateTimeField(blank=True, null=True)
    file = models.FileField(upload_to='quotes/', blank=True, null=True)


class QuotedProductVariant(models.Model):
    pdt_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.CharField(max_length=20, blank=True)
    variant_amount = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-id']


class QuotedProduct(models.Model):
    PRODUCT_STATUS = (
        ('LR', 'LOI Received'),
        ('QS', 'Quotation Submitted'),
        ('QP', 'Quote Prepared'),
        ('SA', 'Submittal Approved'),
        ('OA', 'Order Awaited'),
        ('OR', 'Order Received'),
        ('LT', 'Lost')
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='pdt_quoted', blank=True, null=True)  # product should be mandatory
    variants_quoted = models.ManyToManyField(QuotedProductVariant, blank=True)
    # pdt_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, blank=True, null=True)
    # quote = models.ForeignKey(Quote, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=2, choices=PRODUCT_STATUS, blank=True)
    product_specification = models.TextField(blank=True)
    expected_value = models.PositiveIntegerField(blank=True, null=True)
    eob_date = models.DateField(blank=True, null=True)
    reminder_date = models.DateField(blank=True, null=True)
    quantity = models.CharField(max_length=20, blank=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    quoted_avg_cost = models.CharField(max_length=20, blank=True)
    awarded_comp_name = models.CharField(max_length=20, blank=True)
    awarded_price = models.CharField(max_length=20, blank=True)


class Quote(models.Model):
    STAGES = (
        (1, 'Stage One'),
        (2, 'Stage Two'),
        (3, 'Stage Three'),
        (4, 'Stage Four'),
        (5, 'Stage Five'),
        (6, 'Stage Six'),
    )
    reference_no = models.CharField(max_length=25)
    erp_reference = models.CharField(max_length=25, unique=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="quote_project", blank=True, null=True) # project should be mandatory
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="quote_companies")
    lead = models.ForeignKey(Lead, on_delete=models.PROTECT, blank=True, null=True) # this is not always present, thus project field has been added.If project is present in lead, it should be save in the project field of quote as well
    stage = models.IntegerField(choices=STAGES, default=1)
    currency = models.CharField(max_length=10, blank=True)
    products_quoted = models.ManyToManyField(QuotedProduct, related_name="quote_productss", blank=True)
    revisions = models.ManyToManyField(Revision, related_name="quote_revisions", blank=True)
    terms = models.ForeignKey(Term, on_delete=models.PROTECT)
    quoted_date = models.DateField(auto_now_add=True, blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    net_amount = models.PositiveIntegerField(blank=True, null=True)
    ordered_amount = models.PositiveIntegerField(blank=True, null=True)
    lost_amount = models.PositiveIntegerField(blank=True, null=True)
    in_scope = models.BooleanField(default=True)  # status
    is_active = models.BooleanField(default=True)  # status

    objects = Manager()
    query_objects = CustomQuoteQueryset.as_manager()

    class Meta:
        ordering = ['-id']


class Extension(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
    )
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT, related_name="quote_extensions")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="extended_by")
    status = models.CharField(max_length=2, choices=STATUS, default='P')
    extended_date = models.DateField(blank=True, null=True)
    extended_days = models.CharField(max_length=20, blank=True)


# class Activity(models.Model):
#     user = models.ForeignKey(User, blank=True, null=True)
#     customer = models.ForeignKey(Customer, blank=True, null=True)
#     remark = models.TextField()
#

class Note(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True, related_name='note_project')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True, related_name='note_customer')
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT, blank=True, null=True, related_name='note_quote')
    title = models.CharField(max_length=20, blank=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='note_added_by')

    objects = Manager()
    query_objects = NoteQueryset.as_manager()


class History(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='history_customer', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='history_project', blank=True, null=True)
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT, related_name='history_quote', blank=True, null=True)
    description = models.TextField()
    time = models.DateTimeField(default=django.utils.timezone.now)

    objects = Manager()
    query_objects = CustomHistoryQueryset.as_manager()

    class Meta:
        ordering = ['-time']