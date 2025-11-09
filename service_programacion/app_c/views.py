from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import ProgramacionFisico, ProgramacionFinanciera, Seguimiento
from .serializers import ProgramacionFisicoSerializer, ProgramacionFinancieraSerializer, SeguimientoSerializer
from drf_spectacular.utils import extend_schema


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


class ProgramacionCompletaView(APIView):
    @extend_schema(
        description="Obtiene la programación físico-financiera y seguimiento de un proyecto específico",
        responses={200: dict}
    )
    def get(self, request, proyecto_id):
        fisico = ProgramacionFisico.objects.filter(proyecto_id=proyecto_id).order_by('fecha_inicio')
        financiera = ProgramacionFinanciera.objects.filter(proyecto_id=proyecto_id)
        seguimiento = Seguimiento.objects.filter(proyecto_id=proyecto_id).order_by('fecha_registro')

        return Response({
            "proyecto_id": proyecto_id,
            "programacion_fisica": ProgramacionFisicoSerializer(fisico, many=True).data,
            "programacion_financiera": ProgramacionFinancieraSerializer(financiera, many=True).data,
            "seguimiento": SeguimientoSerializer(seguimiento, many=True).data
        }, status=status.HTTP_200_OK)
