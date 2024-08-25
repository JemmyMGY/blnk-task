from . import views
from django.urls import path

urlpatterns = [
    path('list', views.list_all_customers, name='customers-view-list'),
    path('create', views.sign_up)
]