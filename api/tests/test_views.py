from datetime import date, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Field, Rain


class RainViewSetTest(APITestCase):

    def setUp(self):
        self.test_field = Field.objects.create(
            name='test_field',
            hectares=10,
            latitude=10,
            longitude=10
        )
        self.url = reverse('rain-list')

    def test_create_rain(self):
        data = {'field': 'test_field', 'date': '2020-08-02', 'millimeters': 10}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rain.objects.count(), 1)

        data = {'field': 'fake_field', 'date': '2020-08-02', 'millimeters': 10}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rain.objects.count(), 1)

    def test_list_rain(self):
        Rain.objects.create(
            field=self.test_field,
            date=date.today(),
            millimeters=10
        )
        data = {'field': 'test_field'}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'field': 'fake_field'}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class FieldViewSetTest(APITestCase):

    def setUp(self):
        field = Field.objects.create(
            name='test_field',
            hectares=10,
            latitude=10,
            longitude=10
        )
        Rain.objects.create(field=field, date=date.today(), millimeters=10)
        yesterday = date.today() - timedelta(1)
        Rain.objects.create(field=field, date=yesterday, millimeters=20)
        self.url = reverse('field-list')

    def test_list_average_rain(self):
        data = {'average_rain': 2}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['average_rain'], '15.000')

        data = {'average_rain': 8}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_accumulated_rain(self):
        data = {'accumulated_rain': 20}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['accumulated_rain'], '30.000')

        data = {'accumulated_rain': 31}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
