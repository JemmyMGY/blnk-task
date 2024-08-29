from django.urls import path, include
from . import views

urlpatterns = [
    path('providers/list_all', views.list_all_providers),
    path('providers/add', views.add_provider),
    path('providers/<int:provider_id>/delete', views.delete_provider),
    path('providers/<int:provider_id>/update', views.update_provider),
    path('loans/list_all', views.list_all_loans),

]