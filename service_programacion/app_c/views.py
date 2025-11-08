from rest_framework import generics, permissions
from .models import ProgramacionFisico, ProgramacionFinanciera, Seguimiento
from .serializers import ProgramacionFisicoSerializer, ProgramacionFinancieraSerializer, SeguimientoSerializer


class ProgramacionFisicoListCreateView(generics.ListCreateAPIView):
    queryset = ProgramacionFisico.objects.all()
    serializer_class = ProgramacionFisicoSerializer
    permission_classes = [permissions.AllowAny]


class ProgramacionFisicoRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProgramacionFisico.objects.all()
    serializer_class = ProgramacionFisicoSerializer
    permission_classes = [permissions.AllowAny]


class ProgramacionFinancieraListCreateView(generics.ListCreateAPIView):
    queryset = ProgramacionFinanciera.objects.all()
    serializer_class = ProgramacionFinancieraSerializer
    permission_classes = [permissions.AllowAny]


class ProgramacionFinancieraRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProgramacionFinanciera.objects.all()
    serializer_class = ProgramacionFinancieraSerializer
    permission_classes = [permissions.AllowAny]


class SeguimientoListCreateView(generics.ListCreateAPIView):
    queryset = Seguimiento.objects.all()
    serializer_class = SeguimientoSerializer
    permission_classes = [permissions.AllowAny]
