from rest_framework import serializers

from .models import *
from ..products.models import ProductCategory
# from ..users.serializers import UserSerializer


class CountrySerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Country model.
    """
    class Meta:
        model = Country
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Company model.
    """
    country_details = CountrySerializer(source='country', read_only=True)
    employee_count = serializers.SerializerMethodField()
    quote_count = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    logo = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    header_img = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    footer_img = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'code', 'address1', 'address2', 'phone', 'fax', 'email', 'country', 'website',
                  'is_active', 'enable_reports', 'is_group', 'header_img', 'footer_img', 'employee_count', 'color',
                  'quote_count', 'order_count', 'country_details', 'categories']
        

    def get_employee_count(self, obj):
        try:
            return obj.user_company.count()
        except:
            return 0

    def get_quote_count(self, obj):
        try:
            return obj.quote_companies.count()
        except:
            return 0

    def get_order_count(self, obj):
        return 0

    def get_categories(self, obj):
        return {"categories": ProductCategory.objects.filter(company=obj).values('id', 'name', 'company', 'legendLabel',
                                                    'legendValue', 'tooltip') ,\
                              "no_of_categories":ProductCategory.objects.filter(company=obj).count()}


# class ManufacturerRevisionSerializer(serializers.ModelSerializer):
#     """
#     Custom Serializer for Manufacturer model.
#     """
#     # revised_by_details = UserSerializer(source='revision_by', read_only=True)

#     class Meta:
#         model = ManufacturerRevision
#         fields = ['id', 'revision_by', 'revision_date', 'revised_cost']
#         extra_kwargs = {
#             "id": {
#                 "read_only": True,
#             },
#         }


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Manufacturer model.
    """
    # mfr_rev_details = ManufacturerRevisionSerializer(source='mfr_revisions', many=True)
    # company_details = CompanySerializer(source='company', read_only=True)
    # revision_count = serializers.SerializerMethodField()
    logo = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'website', 'logo', 'is_active', 'mfr_part_code']

    # def get_revision_count(self, obj):
    #     return obj.mfr_revisions.count()

    # @staticmethod
    # def setup_eager_loading(queryset):
    #     """
    #     Performs necessary eager loading of data.
    #     """
    #     # select_related for "to-one" relationships.
    #     queryset = queryset.prefetch_related('mfr_revisions')
    #     return queryset

    # def create(self, validated_data):
    #     """
    #     Custom create method to handle many to many relationships.
    #     """
    #     revisions = validated_data.pop('mfr_revisions', None)

    #     instance = super(ManufacturerSerializer, self).create(validated_data)

    #     if revisions:
    #         revision_objs = (ManufacturerRevision(**rev) for rev in revisions)
    #         objs = ManufacturerRevision.objects.bulk_create(revision_objs)
    #         instance.mfr_revisions.set(objs)
    #     instance.save()

    #     return instance

    # def update(self, instance, validated_data):
    #     """
    #     Custom update method for handling to-many & to-one relationships,
    #     create/delete notifications, handling asynchronous tasks.
    #     """
    #     revisions = validated_data.pop('revisions', None)

    #     if revisions or revisions == []:
    #         instance.revisions.clear()
    #         revision_objs = (ManufacturerRevision(**rev) for rev in revisions)
    #         objs = ManufacturerRevision.objects.bulk_create(revision_objs)
    #         instance.mfr_revisions.set(objs)

    #     instance = super(ManufacturerSerializer, self).update(instance, validated_data)
    #     return instance


class TermSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Term model.
    """
    class Meta:
        model = Term
        fields = '__all__'
