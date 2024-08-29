from rest_framework import serializers
from .models import Customer, LoanRequest

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude  = ['password']

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()