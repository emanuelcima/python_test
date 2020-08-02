from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Sum, Q
from django.db.models.functions import Coalesce 
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from api.models import Field, Rain
from api.serializers import RainSerializer, FieldSerializer, QueryParamsSerializer


class RainViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Creates and lists rain per field
    """
    serializer_class = RainSerializer
    queryset = Rain.objects.none()

    def list(self, request, format=None):
        field = self.request.query_params.get('field', None)
        queryset = Rain.objects.filter(field__name=field)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FieldViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Returns a list of the fields
    """
    serializer_class = FieldSerializer
    query_params_serializer = QueryParamsSerializer

    def get_queryset(self):
        query_params = self.query_params_serializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        if (acum := query_params.data.get('accumulated_rain', None)):
            return self.get_fields_with_accum_rain_greater_than(acum)

        if (days := query_params.data.get('average_rain', None)):
            return self.get_average_rain(days)

        return Field.objects.none()

    def get_fields_with_accum_rain_greater_than(self, accum):
        return Field.objects.annotate(
                accumulated_rain=Sum('rain__millimeters')
        ).filter(accumulated_rain__gt=accum)

    def get_average_rain(self, days):
        today = date.today()
        date_filter = Q(rain__date__gt=today-timedelta(days))
        average = Sum('rain__millimeters', filter=date_filter)/days
        return Field.objects.annotate(average_rain=Coalesce(average, 0))
