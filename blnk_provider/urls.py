from django.urls import path
from . import views

urlpatterns = [
    path('customers/list_all', views.list_all_customers),
    path('loan_requests/list_all', views.list_all_loans_requests),
    path('loan_requests/<int:loan_request_id>/accept', views.accept_loan_request),
    path('loan_requests/<int:loan_request_id>/reject', views.reject_loan_request),
]