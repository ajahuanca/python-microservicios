from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Proyecto
from .serializers import ProyectoSerializer
from .clients import get_empresa, get_programacion
import pybreaker


class ProyectoListCreateView(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]


class ProyectoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_proyecto(request, proyecto_id):
    try:
        proyecto = Proyecto.objects.get(id=proyecto_id)
    except Proyecto.DoesNotExist:
        return Response({'detail': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    # Obtener empresa y programacion (con retry + circuit breaker)

    empresa = None
    programacion = None
    try:
        empresa = get_empresa(proyecto.empresa_id)
    except pybreaker.CircuitBreakerError:
        empresa = {'error': 'Service A unavailable (circuit open)'}
    except Exception as e:
        empresa = {'error': str(e)}

    try:
        programacion = get_programacion(proyecto.id)
    except pybreaker.CircuitBreakerError:
        programacion = {'error': 'Service C unavailable (circuit open)'}
    except Exception as e:
        programacion = {'error': str(e)}

    serializer = ProyectoSerializer(proyecto)
    return Response({
        'proyecto': serializer.data,
        'empresa': empresa,
        'programacion': programacion
    })
