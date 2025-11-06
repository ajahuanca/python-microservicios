from django.urls import path
from .views import EmpresaListCreateView, EmpresaRetrieveUpdateDestroyView


urlpatterns = [
    path('', EmpresaListCreateView.as_view(), name='empresa-list-create'),
    path('<int:pk>/', EmpresaRetrieveUpdateDestroyView.as_view(), name='empresa-rud'),
]