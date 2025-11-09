from django.urls import path
from .views import ProyectoListCreateView, ProyectoRetrieveUpdateDestroyView, ProyectoDetailView


urlpatterns = [
    path('', ProyectoListCreateView.as_view(), name='proyecto-list-create'),
    path('<int:pk>/', ProyectoRetrieveUpdateDestroyView.as_view(), name='proyecto-rud'),
    path('detalle/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto-detalle'),
]
