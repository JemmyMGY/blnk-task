from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Provider, Loan
from .serializers import ProviderSerializer, LoanSerializer

@api_view(['GET'])
def list_all_providers(request):
    all_providers = Provider.objects.all()
    serialized_providers = ProviderSerializer(all_providers, many=True)
    return Response(serialized_providers.data)

@api_view(['POST'])
def add_provider(request):
    provider = Provider(name=request.data.get('name'), email=request.data.get('email'), total_fund=float(request.data.get('total_fund')))

    try:
        provider.save()
        serialized_provider = ProviderSerializer(provider)
        return Response(serialized_provider.data, status=201)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

@api_view(['DELETE'])
def delete_provider(request, provider_id):
    try:
        provider = Provider.objects.get(id=provider_id)
        provider_name = provider.name
        provider.delete()
        return Response({"message": "Provider with id: {} and name: {} has been deleted successfully".format(provider_id, provider_name)}, status=200)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

@api_view(['PATCH'])
def update_provider(request, provider_id):
    new_name = request.data.get('name')
    new_fund = float(request.data.get('total_fund'))
    try:
        provider = Provider.objects.get(id=provider_id)
        provider.total_fund = new_fund
        provider.name = new_name
        provider.save()
        return Response({"message": "Provider updated successfully"}, status=200)
    except Exception as e:
        error = {
            "error message": str(e)
        }
        return Response(error, status=400)

@api_view(['GET'])
def list_all_loans(request):
    all_loans = Loan.objects.all()
    serialized_loans = LoanSerializer(all_loans, many=True)
    return Response(serialized_loans.data)