from django.urls import path
from .views import (
    ProgramacionFisicoListCreateView, ProgramacionFisicoRUDView,
    ProgramacionFinancieraListCreateView, ProgramacionFinancieraRUDView,
    SeguimientoListCreateView
)


urlpatterns = [
    path('fisico/', ProgramacionFisicoListCreateView.as_view(), name='fisico-list-create'),
    path('fisico/<int:pk>/', ProgramacionFisicoRUDView.as_view(), name='fisico-rud'),
    path('financiera/', ProgramacionFinancieraListCreateView.as_view(), name='financiera-list-create'),
    path('financiera/<int:pk>/', ProgramacionFinancieraRUDView.as_view(), name='financiera-rud'),
    path('seguimiento/', SeguimientoListCreateView.as_view(), name='seguimiento-list-create'),
]
