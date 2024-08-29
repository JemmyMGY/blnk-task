from telnetlib import STATUS

from django.test import TestCase
from rest_framework.test import APIClient

from bank.models import Loan, Payment, Provider
from customers.models import Customer, LoanRequest


class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Customer(full_name="John Doe", email="xyz@abc.com", password="12345678").save()
        Provider(name="Bank", email="blnk@test.com", total_fund=10_000_000).save()

    def test_customer_creation(self):
        response = self.client.post('/customers/create', {
            "full_name": "John Doe",
            "email": "abc@test.co",
            "password": "12345678"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.count(), 2)

    def test_customer_request_loan(self):
        customer = Customer.objects.get(id=1)
        response = self.client.post('/customers/{}/loan_requests/request'.format(customer.id), {
            "amount": 500000,
            "duration": 12
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LoanRequest.objects.get(customer=customer).amount, 500000)
        self.assertEqual(LoanRequest.objects.get(customer=customer).duration, 12)

    def test_make_loan_payment(self):
        customer = Customer.objects.get(id=1)
        blnk_provider = Provider.objects.get(email="blnk@test.com")
        loan_request = LoanRequest(customer=customer, amount=500_000, duration=12, status="APPROVED")
        loan_request.save()
        loan = Loan(provider= blnk_provider, loan_request=loan_request, customer=customer, total_amount=500000, remaining_amount=500000, status="APPROVED", duration=12)
        loan.save()

        response = self.client.post('/customers/{}/loan_requests/{}/payment'.format(customer.id, loan_request.id), {
            "payment_amount": 100_000
        })

        updated_loan = Loan.objects.get(loan_request=loan_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_loan.remaining_amount, 400_000)
        self.assertEqual(Payment.objects.get(loan=updated_loan).customer, customer)