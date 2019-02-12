from rest_framework import serializers

from paranuara.models import People


class CompanyEmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('_id', 'name', 'email')