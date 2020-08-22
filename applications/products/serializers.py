from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *
from ..common.serializers import ManufacturerSerializer, CompanySerializer, CountrySerializer
from ..users.serializers import UserSerializer


class ProductUnitSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for ProductCategory model.
    """
    class Meta:
        model = ProductUnit
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for FileUpload model.
    """
    class Meta:
        model = FileUpload
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Custom Serializer for ProductCategory model.
    """
    category_company_details = CompanySerializer(source='company', read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'company', 'legendLabel', 'legendValue', 'tooltip', 'products',
                 'category_company_details']

    def get_products(self, obj):
        return Product.objects.filter(category=obj).values('id', 'name', 'image', 'category', 'company',
                                 'manufacturer', 'is_active', 'sales_engineers', 'remarks')


class ProducttSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Productt model.
    """
    company_details = CompanySerializer(source='company', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'company', 'company_details']


class AvgCostRevisionSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Revision model.
    """
    revision_by_details = UserSerializer(source='revision_by', read_only=True)

    class Meta:
        model = AvgCostRevision
        fields = ['id', 'revision_by', 'revision_date', 'revision_by_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for ProductVariant model.
    """
    product_details = ProducttSerializer(source='product', read_only=True)
    unit_details = ProductUnitSerializer(source='unit', read_only=True)
    country_details = CountrySerializer(source='origin_country', read_only=True)
    avg_cost_revision_details = AvgCostRevisionSerializer(source='avg_cost_revisions', many=True, required=False)
    no_of_revisions = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'description', 'note', 'product_code', 'manufacturer_part_code', 'unit', 'average_cost',
                  'min_sales_price', 'origin_country', 'runit_price', 'avg_cost_revisions', 'old_average_cost',
                  'unit_details', 'country_details', 'product_details', 'avg_cost_revision_details', 'no_of_revisions']
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
        queryset = queryset.prefetch_related('avg_cost_revisions')
        return queryset

    def get_no_of_revisions(self, obj):
        # extended date - today
        return obj.avg_cost_revisions.count()

    def update(self, instance, validated_data):
        """
        Custom update method for handling to-many & to-one relationships,
        create/delete notifications, handling asynchronous tasks.
        """
        avg_cost_revisions = validated_data.pop('avg_cost_revisions', None)

        if avg_cost_revisions or avg_cost_revisions == []:
            arevision_objs = (AvgCostRevision(**arev) for arev in avg_cost_revisions)
            objs = AvgCostRevision.objects.bulk_create(arevision_objs)
            instance.avg_cost_revisions.set(objs)

        instance = super(ProductVariantSerializer, self).update(instance, validated_data)
        return instance


class ProductSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Product model.
    """
    category_details = ProductCategorySerializer(source='category', read_only=True)
    company_details = CompanySerializer(source='company', read_only=True)
    pdt_variant_details = ProductVariantSerializer(source='productvariant_set', many=True, required=False)
    manufacturer_details = ManufacturerSerializer(source='manufacturer', read_only=True)
    sales_engineer_details = UserSerializer(source='sales_engineers', read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'category', 'company', 'manufacturer', 'is_active', 'sales_engineers', 'remarks',
                  'to_append', 'category_details', 'company_details', 'manufacturer_details', 'sales_engineer_details',
                  'pdt_variant_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    @staticmethod
    def setup_eager_loading(queryset):
        """
        Performs necessary eager loa=ding of data.
        """
        # select_related for "to-one" relationships.
        queryset = queryset.prefetch_related('productvariant_set')
        return queryset

    def create(self, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        variants = validated_data.pop('productvariant_set', None)
        instance = super(ProductSerializer, self).create(validated_data)
        if instance.to_append:
            instance.name = instance.name + instance.manufacturer.name
        if variants:
            variant_objs = (ProductVariant(**var) for var in variants)
            objs = ProductVariant.objects.bulk_create(variant_objs)
            for i in objs:
                i.product = instance
                i.save()
        instance.save()
        return instance

