from rest_framework import serializers

from .models import User
from ..common.serializers import CompanySerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for User model.
    """
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=False, allow_null=True)
    company_details = CompanySerializer(source='company', read_only=True)
    assigned_company_details = CompanySerializer(source='assigned_companies', read_only=True, many=True)
    reporting_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'email', 'phone', 'telephone', 'employee_code',
                  'designation', 'role', 'company', 'department', 'reporting', 'photo', 'assigned_companies',
                  'company_details', 'is_active', 'reporting_name', 'assigned_company_details']
        extra_kwargs = {
            "id": {
                "read_only": True,
            },

        }

    def get_reporting_name(self, obj):
        try:
            return obj.reporting.first_name
        except:
            return None

    def create(self, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        instance = super(UserSerializer, self).create(validated_data)
        instance.save()
        instance.set_password(instance.password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Custom create method to handle many to many relationships.
        """
        instance = super(UserSerializer, self).update(instance, validated_data)
        instance.save()
        instance.set_password(instance.password)
        instance.save()
        return instance
