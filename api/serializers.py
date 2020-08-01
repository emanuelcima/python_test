from rest_framework import serializers
from kilimo.models import Field, Rain


class RainSerializer(serializers.ModelSerializer):
    """Rain Serializer"""

    class Meta:
        model = Rain
        fields = ['date', 'millimeters', 'field']


class FieldSerializer(serializers.ModelSerializer):
    """Field Serializer"""

    accumulated_rain = serializers.DecimalField(
        max_digits=10,
        decimal_places=3,
        required=False
    )

    average_rain = serializers.DecimalField(
        max_digits=10,
        decimal_places=3,
        required=False
    )

    class Meta:
        model = Field
        fields = [
            'name',
            'hectares',
            'latitude',
            'longitude',
            'accumulated_rain',
            'average_rain'
        ]
