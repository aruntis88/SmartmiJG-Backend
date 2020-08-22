from rest_framework import serializers

from .models import Customer, Contact, CustomerType
from ..common.serializers import CountrySerializer
from ..users.serializers import UserSerializer
from ..projects.models import History


class ContactSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Contact model.
    """
    class Meta:
        model = Contact
        fields = '__all__'


class CustomerTypeSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Contact model.
    """
    class Meta:
        model = CustomerType
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for Customer model.
    """
    contact_details = ContactSerializer(source='point_of_contact', many=True)
    customer_type_details = CustomerTypeSerializer(source='customer_type', many=True, read_only=True)
    country_details = CountrySerializer(source='country', read_only=True)
    introby_details = UserSerializer(source='introduced_by', read_only=True)
    sales_engineers_details = UserSerializer(source='sales_engineers', many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'type', 'email', 'fax', 'phone', 'address1', 'address2', 'country', 'website', 'is_active',
                  'introduced_by', 'introduced_date', 'point_of_contact', 'sales_engineers', 'contact_details',
                  'country_details', 'introby_details','customer_type', 'customer_type_details', 'sales_engineers_details']
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
        queryset = queryset.prefetch_related('point_of_contact')
        return queryset

    def create(self, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        point_of_contact = validated_data.pop('point_of_contact', None)

        instance = super(CustomerSerializer, self).create(validated_data)

        if point_of_contact:
            contact_objs = (Contact(**contact) for contact in point_of_contact)
            objs = Contact.objects.bulk_create(contact_objs)
            instance.point_of_contact.set(objs)

        instance.save()

        return instance

    def update(self, instance, validated_data):
        """
        Custom update method for handling to-many & to-one relationships,
        create/delete notifications, handling asynchronous tasks.
        """
        point_of_contact = validated_data.pop('point_of_contact', None)

        if point_of_contact or point_of_contact == []:
            instance.point_of_contact.clear()
            contact_objs = (Contact(**contact) for contact in point_of_contact)
            objs = Contact.objects.bulk_create(contact_objs)
            instance.point_of_contact.set(objs)
        old_obj = Customer.objects.get(id=instance.id)
        instance = super(CustomerSerializer, self).update(instance, validated_data)
        for field in [f for f in instance._meta.get_fields()
                      if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)]:
            try:
                if getattr(old_obj, field.name) != getattr(instance, field.name):
                    description = "{} has changed {} from {} to {}".format(self.context['request'].user, field.name,
                                                            getattr(old_obj, field.name), getattr(instance, field.name))
                    History.objects.create(customer=instance, description=description)
            except Exception:
                pass
        return instance
