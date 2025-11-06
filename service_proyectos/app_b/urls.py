from django.urls import path
from .views import ProyectoListCreateView, ProyectoRetrieveUpdateDestroyView, detalle_proyecto


urlpatterns = [
    path('', ProyectoListCreateView.as_view(), name='proyecto-list-create'),
    path('<int:pk>/', ProyectoRetrieveUpdateDestroyView.as_view(), name='proyecto-rud'),
    path('detalle/<int:proyecto_id>/', detalle_proyecto, name='proyecto-detalle'),
]
