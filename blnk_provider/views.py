from django.shortcuts import render
from rest_framework.decorators import api_view

from customers.models import Customer, LoanRequest
from bank.models import Loan, Provider
from customers.serializers import CustomerSerializer
from rest_framework.response import Response
from customers.serializers import LoanRequestSerializer

BLNK_PROVIDER_ID = 1


@api_view(['GET'])
def list_all_customers(request):
    all_customers = Customer.objects.all()
    serialized_customers = CustomerSerializer(all_customers, many=True)
    return Response(serialized_customers.data)


@api_view(['GET'])
def list_all_loans_requests(request):
    all_loans = LoanRequest.objects.all()
    serialized_loans = LoanRequestSerializer(all_loans, many=True)
    return Response(serialized_loans.data)


def handle_bank_loan_request(loan_request):
    try:
        provider = Provider.objects.get(id=BLNK_PROVIDER_ID)
        bank_loan = Loan(
            loan_request=loan_request,
            customer=loan_request.customer,
            provider=provider,
            total_amount=loan_request.amount,
            status=loan_request.status,
            duration=loan_request.duration,
        )
        bank_loan.save()
        provider.total_fund -= loan_request.amount
        provider.save()

        return True

    except Exception as e:
        return str(e)


@api_view(['PATCH'])
def accept_loan_request(request, loan_request_id):
    try:
        loan_req = LoanRequest.objects.get(id=loan_request_id)

        if  loan_req.status == "APPROVED":
            return Response({"message": "Loan request has already been approved"}, status=200)
        elif loan_req.status == "REJECTED":
            return Response({"error": "Loan request has already been rejected and can't be approved"}, status=400)

        if Provider.objects.get(id=BLNK_PROVIDER_ID).total_fund < LoanRequest.objects.get(id=loan_request_id).amount:
            return Response({"error": "Insufficient funds"}, status=400)


        loan_req.status = "APPROVED"
        loan_req.save()

        bank_response = handle_bank_loan_request(loan_req)

        if bank_response is True:
            return Response({"message": "Loan request approved and sent to the bank"}, status=200)

        return Response({"message": "Loan request approved and sent to the bank", "bank_response": bank_response},
                        status=200)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)


@api_view(['PATCH'])
def reject_loan_request(request, loan_request_id):
    try:
        loan_req = LoanRequest.objects.get(id=loan_request_id)
        if loan_req.status == "REJECTED":
            return Response({"message": "Loan request has already been rejected"}, status=200)
        elif loan_req.status == "APPROVED":
            return Response({"error": "Loan request has already been rejected and can't be approved"}, status=400)

        loan_req.status = "REJECTED"
        loan_req.save()
        return Response({"message": "Loan request rejected"}, status=200)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)
