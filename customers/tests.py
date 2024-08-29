from django.test import TestCase
from rest_framework.test import APIClient

from customers.models import Customer


class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Customer(full_name="John Doe", email="xyz@test.co", password="12345678").save()

