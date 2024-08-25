from django.shortcuts import render
from .models import Customer
# Create your views here.


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CustomerSerializer


@api_view(['GET'])
def list_all_customers(request):
    all_customers = Customer.objects.all()
    serialized_customers = CustomerSerializer(all_customers, many= True)
    return Response(serialized_customers.data)

@api_view(['POST'])
def sign_up(request):
    customer_name =  request.data.get('full_name')
    customer_email = request.data.get('email')
    customer_password = request.data.get('password')
    customer = Customer(full_name = customer_name, email = customer_email, password = customer_password)
    if customer.save():
        serialized_customer = CustomerSerializer(customer)
        return Response(serialized_customer)
    failed = {
        "error": "failed to save the customer" 
    }
    return Response(failed, status = 400)