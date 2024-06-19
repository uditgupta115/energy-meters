import os
import pytest
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command

from plugins.clients.carrots.models import SupplyPoint
from tests.conftest import carrots_readings_file_path


# Create your tests here.
class CarrotReadingTestCase(TestCase):
    def setUp(self):
        call_command(
            "ingest_readings_file",
            "carrots",
            os.path.join(
                settings.BASE_DIR,
                "tests/fixtures/carrots/readings.txt",
            )
        )
        self.headers = {'App-Id': 'ff26fe53-5638-4c81-9957-1c7537d7eb48'}
        self.client = Client()
        self.url = reverse(
            'readings_v2', args=('0300111001601606083625', )
        )

    def test_get_with_app_id_header(self):
        response = self.client.get(self.url, headers=self.headers)
        # print(SupplyPoint.objects.values('identifier'))
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), True)
        self.assertEqual(len(response.json().get('data')), 3)

    def test_get_without_app_id_header(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'status': False,
                "error": 'App-Id header is missing!'
            }
        )

    def test_get_without_app_id_header(self):
        response = self.client.get(
            self.url, headers={'App-Id': "ff2afe53-5638-4c81-9957-1c7537d7eb48"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'status': False,
                "error": "Not a valid Client App-Id"
            }
        )

    def test_with_invalid_supply_point_for_client(self):
        self.url = reverse(
            'readings_v2', args=('UD0300111001601606083625', )
        )

        response = self.client.get(self.url, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'status': False,
                "error": 'Not a valid Supply Point!'
            }
        )
