from . import views
from django.urls import path

urlpatterns = [
    path('create', views.sign_up),
    path('authenticate', views.authenticate),
    path('<int:customer_id>/loan_requests/request', views.request_loan),
    path('<int:customer_id>/loan_requests/list', views.list_customer_loan_requests),
    path('<int:customer_id>/loan_requests/<int:loan_request_id>/payment', views.make_payment),
]