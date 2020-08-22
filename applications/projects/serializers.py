import datetime
import json

from rest_framework import serializers

from .models import *
from ..common.models import Company
from ..common.serializers import CountrySerializer, CompanySerializer
from ..customers.serializers import CustomerSerializer
from ..products.serializers import ProductSerializer, ProductVariantSerializer, ProductCategorySerializer
from ..users.serializers import UserSerializer


class ProjectSegmentSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for ProjectSegment model.
    """

    class Meta:
        model = ProjectSegment
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Project model.
    """
    country_details = CountrySerializer(source='country', read_only=True)
    companies_linked_details = CompanySerializer(source='companies_linked', read_only=True, many=True)
    main_contractor_details = CustomerSerializer(source='main_contractor', read_only=True)
    main_sub_contractor_details = CustomerSerializer(source='main_sub_contractor', read_only=True)
    client_details = CustomerSerializer(source='client', read_only=True)
    design_consultant_details = CustomerSerializer(source='design_consultant', read_only=True)
    supervision_consultant_details = CustomerSerializer(source='supervision_consultant', read_only=True)
    intro_by_details = UserSerializer(source='intro_by', read_only=True)
    segment_details = ProjectSegmentSerializer(source='segment', read_only=True)
    quoted_companies = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'reference_no', 'name', 'stage', 'status', 'segment', 'value', 'location',
                  'country', 'companies_linked', 'intro_by', 'intro_date', 'completion', 'exp_start_date', 'exp_end_date',
                  'main_contractor', 'main_sub_contractor', 'client', 'design_consultant', 'supervision_consultant',
                  'latitude', 'longitude', 'main_contractor_details', 'main_sub_contractor_details', 'client_details',
                  'design_consultant_details', 'supervision_consultant_details', 'companies_linked_details',
                  'country_details', 'intro_by_details', 'segment_details', 'quoted_companies']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    def get_quoted_companies(self, obj):
        response = []
        try:
            for comp in Company.objects.all():
                q_objs = Quote.objects.filter(project=obj, company=comp)
                if q_objs :
                    response.append({"company": comp.name, "detail": q_objs.values('company__name', 'net_amount',
                                                        'ordered_amount', 'lost_amount', 'in_scope')})
                else:
                    response.append({"company": comp.name, "detail": [{"company__name": comp.name, "net_amount": None,
                                                        "ordered_amount": None, "lost_amount": None, "in_scope": None}]})
            return response
        except:
            return None

    def create(self, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        instance = super(ProjectSerializer, self).create(validated_data)
        try:
            instance.companies_linked = [i.id for i in Company.objects.all()]
        except:
            objs = Company.objects.all()
            instance.companies_linked.set(objs)
        # instance.reference_no = instance.sales_engineer.company.name[:3] + "-" + '%05d' % instance.id
        instance.reference_no = "JGP-" + '%05d' % instance.id
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        old_obj = Project.objects.get(id=instance.id)
        instance = super(ProjectSerializer, self).update(instance, validated_data)
        # instance.reference_no = instance.sales_engineer.company.name[:3] + "-" + '%05d' % instance.id

        for field in [f for f in instance._meta.get_fields()
                      if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)]:
            try:
                if getattr(old_obj, field.name) != getattr(instance, field.name):
                    description = "{} has changed {} from {} to {}".format(self.context['request'].user, field.name,
                                                            getattr(old_obj, field.name), getattr(instance, field.name))
                    History.objects.create(project=instance, description=description)
            except:
                pass
        instance.reference_no = "JGP-" + '%05d' % instance.id
        instance.save()
        return instance


class LeadSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Lead model.
    """
    customer_details = CountrySerializer(source='customer', read_only=True)
    company_details = CompanySerializer(source='company', read_only=True)
    project_details = ProjectSerializer(source='project', read_only=True)
    sales_engineer_details = UserSerializer(source='sales_engineer', read_only=True)
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)
    description_details = ProductCategorySerializer(source='description', read_only=True, many=True)

    class Meta:
        model = Lead
        fields = ['id', 'reference_no', 'customer', 'project', 'lead_source', 'sales_engineer', 'assigned_to', 'assigned_to',
                  'due_date', 'contact_name', 'email', 'phone', 'description', 'company', 'customer_details', 'project_details',
                  'sales_engineer_details', 'assigned_to_details', 'company_details', 'description_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        instance = super(LeadSerializer, self).create(validated_data)
        try:
            instance.reference_no = "LG-" + str(datetime.datetime.now().year)[2:] + "-" +\
                                instance.sales_engineer.company.name[:3] + "-" + '%05d' % instance.id
        except:
            instance.reference_no = "LG-" + str(datetime.datetime.now().year)[2:] + "-" + \
                                    "JRS" + "-" + '%05d' % instance.id
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        instance = super(LeadSerializer, self).update(instance, validated_data)
        try:
            instance.reference_no = "LG-" + str(datetime.datetime.now().year)[2:] + "-" +\
                                instance.company.name[:3] + "-" + '%05d' % instance.id
        except:
            instance.reference_no = "LG-" + str(datetime.datetime.now().year)[2:] + "-" +\
                                "JRS" + "-" + '%05d' % instance.id

        instance.save()
        return instance


class RevisionSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Revision model.
    """
    revision_by_details = UserSerializer(source='revision_by', read_only=True)

    class Meta:
        model = Revision
        fields = ['id', 'revision_by', 'revision_date', 'file', 'revision_by_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }


class QuotedProductVariantSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Product model.
    """
    variant_details = ProductVariantSerializer(source='pdt_variant', read_only=True)

    class Meta:
        model = QuotedProductVariant
        fields = ['id', 'pdt_variant', 'quantity', 'variant_amount', 'variant_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }


class QuotedProductSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Product model.
    """
    # quote_details = QuoteSerializer(source='quote', read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)
    # variant_details = ProductVariantSerializer(source='pdt_variant', read_only=True)
    variants_quoted_details = QuotedProductVariantSerializer(source='variants_quoted', many=True, required=False)

    class Meta:
        model = QuotedProduct
        fields = ['id', 'product', 'status', 'product_specification', 'expected_value', 'eob_date', 'reminder_date',
                  'amount', 'product_details', 'quoted_avg_cost', 'variants_quoted',
                  'variants_quoted_details', 'awarded_comp_name', 'awarded_price']
        # , 'variant_details', 'pdt_variant', 'quantity', 'quote'
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    @staticmethod
    def setup_eager_loading(queryset):
        """
        Performs necessary eager loading of data.
        """
        # select_related for "to-one" relationships.
        queryset = queryset.prefetch_related('variants_quoted')
        return queryset

    def update(self, instance, validated_data):
        """
        Custom update method for handling to-many & to-one relationships,
        create/delete notifications, handling asynchronous tasks.
        """
        variants = validated_data.pop('variants_quoted', None)

        if variants or variants == []:
            instance.variants_quoted.clear()
            variant_objs = (QuotedProductVariant(**var) for var in variants)
            objs = QuotedProductVariant.objects.bulk_create(variant_objs)
            instance.variants_quoted.add(objs)

        instance = super(QuotedProductSerializer, self).update(instance, validated_data)
        return instance


class QuoteSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Quote model.
    """
    revision_details = RevisionSerializer(source='revisions', many=True, required=False)
    company_details = CompanySerializer(source='company', read_only=True)
    lead_details = LeadSerializer(source='lead', read_only=True)
    sales_engineer_details = UserSerializer(source='sales_engineer', read_only=True)
    quoted_product_details = QuotedProductSerializer(source='products_quoted', many=True, required=False)
    # variant_quoted_details = QuotedProductVariantSerializer(source='products_quoted__variants_quoted', many=True, required=False)
    # product_variant_details = QuotedProductSerializer(source='quotedproduct_set', many=True, required=False)
    project_details = ProjectSerializer(source='project', read_only=True)
    remaining_days = serializers.SerializerMethodField()
    # calculate_net = serializers.SerializerMethodField()
    extensions = serializers.SerializerMethodField()
    no_of_revisions = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = ['id', 'reference_no', 'erp_reference', 'company', 'lead','project', 'stage', 'currency', 'terms', 'quoted_date',
                  'company_details', 'lead_details', 'sales_engineer_details', 'remaining_days', 'revisions', 'no_of_revisions',
                  'revision_details', 'discount', 'net_amount', 'products_quoted', 'project_details', 'extensions',
                  'ordered_amount', 'lost_amount', 'in_scope', 'is_active', 'quoted_product_details']
        # , 'calculate_net', 'product_variant_details'
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    def get_remaining_days(self, obj):
        # extended date - today
        return 5

    def get_no_of_revisions(self, obj):
        # extended date - today
        return obj.revisions.count()

    def get_extensions(self, obj):
        try:
            return {
                "extensions": Extension.objects.filter(quote=obj).values('id', 'requested_by__first_name',
                                                                         'requested_by__last_name', 'status', 'extended_date', 'extended_days'),
                "no_of_extensions": obj.quote_extensions.count()
            }

        except:
            return None

    # def get_calculate_net(self, obj):
    #     products = Product.objects.filter(productvariant__quotedproduct__quote=obj).distinct() | Product.objects.\
    #         filter(quotedproduct__quote=obj).distinct()
    #     variants=[]
    #     for i in products:
    #         qq = QuotedProduct.objects.filter(pdt_variant__product=i, quote=obj)
    #         variants.append({ i.name : [{"variant" : j.pdt_variant.description,
    #                                "quantity": j.quantity, "quoted_avg_cost": j.quoted_avg_cost} for j in qq]})
    #
    #     return variants



    @staticmethod
    def setup_eager_loading(queryset):
        """
        Performs necessary eager loading of data.
        """
        # select_related for "to-one" relationships.
        queryset = queryset.prefetch_related('revisions', 'products_quoted')
        return queryset

    def create(self, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        revisions = validated_data.pop('revisions', None)
        productss = validated_data.pop('products_quoted', None)
        instance = super(QuoteSerializer, self).create(validated_data)

        if revisions:
            revision_objs = (Revision(**rev) for rev in revisions)
            objs = Revision.objects.bulk_create(revision_objs)
            instance.revisions.set(objs)

        if productss:
            for pdt in productss:
                variant = pdt.pop('variants_quoted', None)
                obj = QuotedProduct.objects.create(**pdt)
                instance.products_quoted.add(obj)
                for v in variant:
                    objj = QuotedProductVariant.objects.create(**v)
                    obj.variants_quoted.add(objj)
                obj.save()
        # QIC / QTN19106322
        try:
            instance.reference_no = instance.company.name[:3] + "/QTN" + '%05d' % instance.id
        except:
            pass

        instance.save()

        return instance

    def update(self, instance, validated_data):
        """
        Custom update method for handling to-many & to-one relationships,
        create/delete notifications, handling asynchronous tasks.
        """
        revisions = validated_data.pop('revisions', None)
        productss = validated_data.pop('products_quoted', None)

        if revisions or revisions == []:
            instance.revisions.clear()
            revision_objs = (Revision(**rev) for rev in revisions)
            objs = Revision.objects.bulk_create(revision_objs)
            instance.revisions.set(objs)

        if productss or productss == []:
            instance.products_quoted.clear()
            for pdt in productss:
                variant = pdt.pop('variants_quoted', None)
                obj = QuotedProduct.objects.create(**pdt)
                instance.products_quoted.add(obj)
                for v in variant:
                    objj = QuotedProductVariant.objects.create(**v)
                    obj.variants_quoted.add(objj)
                obj.save()


        old_obj = Quote.objects.get(id=instance.id)
        instance = super(QuoteSerializer, self).update(instance, validated_data)
        for field in [f for f in instance._meta.get_fields()
                      if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)]:
            try:
                if getattr(old_obj, field.name) != getattr(instance, field.name):
                    description = "{} has changed {} from {} to {}".format(self.context['request'].user, field.name,
                                                            getattr(old_obj, field.name), getattr(instance, field.name))
                    History.objects.create(quote=instance, description=description)
            except:
                pass
        try:
            instance.reference_no = instance.company.name[:3] + "/QTN" + '%05d' % instance.id
            instance.save()
        except:
            pass
        return instance


class ExtensionSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Extension model.
    """
    quote_details = QuoteSerializer(source='quote', read_only=True)
    requested_by_details = UserSerializer(source='requested_by', read_only=True)

    class Meta:
        model = Extension
        fields = ['id', 'quote', 'requested_by', 'status', 'extended_date', 'quote_details', 'extended_days', 'requested_by_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }


class NoteSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for ProjectSegment model.
    """
    project_details = ProjectSerializer(source='project', read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    added_by_details = UserSerializer(source='added_by', read_only=True)

    class Meta:
        model = Note
        fields = ['project', 'customer', 'quote', 'title', 'date', 'description', 'added_by', 'project_details',
                  'customer_details', 'added_by_details']


class HistorySerializer(serializers.ModelSerializer):
    """
    Custom Serializer for ProjectSegment model.
    """
    # project = serializers.SerializerMethodField()
    # customer = serializers.SerializerMethodField()
    # added_by = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = '__all__'


