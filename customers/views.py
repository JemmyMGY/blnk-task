import decimal

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import CustomerSerializer, LoanRequestSerializer, LoginSerializer
from .models import Customer, LoanRequest
from bank.models import Loan, Payment
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def make_payment(request, loan_request_id, customer_id):
    loan_payment = decimal.Decimal(float(request.data.get('payment_amount')))
    try:
        loan_request = LoanRequest.objects.get(id=loan_request_id)
        if loan_request.status == "REJECTED":
            return Response({"error": "Loan request has been rejected and you can't pay for rejected loan"}, status=400)
        elif loan_request.status == "PENDING":
            return Response({"error": "Loan request has not been approved yet"}, status=400)

        loan = Loan.objects.get(loan_request=loan_request)
        if loan_payment > loan.remaining_amount :
            return Response({"error": "Payment amount exceeds remaining loan amount"}, status=400)

        loan.remaining_amount -= loan_payment
        loan.paid_amount += loan_payment
        loan.save()
        Payment(customer=loan.customer, loan=loan, paid_amount=loan_payment).save()
        return Response({"message": "Payment successful"}, status=200)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

@api_view(['GET'])
def list_customer_loan_requests(request, customer_id):
    try:
        all_requests = LoanRequest.objects.filter(customer=customer_id)
        serialized_loans = LoanRequestSerializer(all_requests, many=True)
        return Response(serialized_loans.data, status=200)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

@api_view(['POST'])
def request_loan(request, customer_id):
    loan_data = {}
    loan_data['amount'] = request.data.get('amount')
    loan_data['duration'] = request.data.get('duration')
    loan_data['customer'] = customer_id
    loan_serializer = LoanRequestSerializer(data=loan_data)

    if loan_serializer.is_valid():
        loan_serializer.save()
        return Response(loan_serializer.data, status=201)
    return Response(loan_serializer.errors, status=400)

@api_view(['POST'])
def sign_up(request):
    customer_name = request.data.get('full_name')
    customer_email = request.data.get('email')
    customer_password = request.data.get('password')
    customer = Customer(full_name=customer_name, email=customer_email, password=customer_password)
    try:
        customer.save()
        serialized_customer = CustomerSerializer(customer)
        return Response(serialized_customer.data, status=201)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

@api_view(['POST'])
def authenticate(request):
    login_serializer = LoginSerializer(data=request.data)
    if not login_serializer.is_valid():
        return Response(login_serializer.errors, status=400)
    try:
        customer = Customer.objects.get(email=login_serializer.data['email'])
        if check_password(login_serializer.data['password'], customer.password):
            token = get_tokens_for_user(customer)
            return Response(token, status=200)
        else:
            return Response({"error message": "Invalid credentials"}, status=401)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    return {
        'refresh': str(refresh),
        'access': token
    }

