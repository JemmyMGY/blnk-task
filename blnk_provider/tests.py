from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

from bank.models import Provider
from customers.models import LoanRequest, Customer

class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Customer(full_name="John Doe", email="xyz@test.com", password="12345678").save() #id=1
        Customer(full_name="Sarah Lu", email="abc@test.com", password="12345678").save() #id=2

        LoanRequest(customer_id=1, amount=1000, duration=12).save() #id=1
        LoanRequest(customer_id=1, amount=2000, duration=24, status="REJECTED").save() #id=2
        LoanRequest(customer_id=2, amount=3000, duration=36, status= "APPROVED").save() #id=3
        LoanRequest(customer_id=2, amount=5000, duration=12).save()  # id=4
        Provider(name="BLNK", total_fund=10000, email="blnk@test.ai").save()

    def test_list_all_customers(self):
        response = self.client.get('/blnk_provider/customers/list_all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Customer.objects.count())

    def test_list_all_loans_requests(self):
        response = self.client.get('/blnk_provider/loan_requests/list_all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), LoanRequest.objects.count())

    @patch('blnk_provider.views.handle_bank_loan_request')
    def test_accept_pending_loan_request(self, mocked_handle_bank_loan_request):
        mocked_handle_bank_loan_request.return_value = True

        loan_request = LoanRequest.objects.get(id=1)
        response = self.client.patch('/blnk_provider/loan_requests/{}/accept'.format(loan_request.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Loan request approved and sent to the bank')
        self.assertEqual(LoanRequest.objects.get(id=1).status, 'APPROVED')

    def test_accept_approved_loan_request(self):
        loan_request = LoanRequest.objects.get(id=3)
        response = self.client.patch('/blnk_provider/loan_requests/{}/accept'.format(loan_request.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Loan request has already been approved')

    def test_accept_rejected_loan_request(self):
        loan_request = LoanRequest.objects.get(id=2)
        response = self.client.patch('/blnk_provider/loan_requests/{}/accept'.format(loan_request.id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Loan request has already been rejected and can\'t be approved')

    def test_reject_pending_loan_request(self):
        loan_request = LoanRequest.objects.get(id=4)
        response = self.client.patch('/blnk_provider/loan_requests/{}/reject'.format(loan_request.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Loan request rejected')
        self.assertEqual(LoanRequest.objects.get(id=4).status, 'REJECTED')

    def test_reject_rejected_loan_request(self):
        loan_request = LoanRequest.objects.get(id=2)
        response = self.client.patch('/blnk_provider/loan_requests/{}/reject'.format(loan_request.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Loan request has already been rejected')
        self.assertEqual(loan_request.status, 'REJECTED')

    def test_reject_approved_loan_request(self):
        loan_request = LoanRequest.objects.get(id=3)
        response = self.client.patch('/blnk_provider/loan_requests/{}/reject'.format(loan_request.id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Loan request has already been rejected and can\'t be approved')
        self.assertEqual(loan_request.status, 'APPROVED')