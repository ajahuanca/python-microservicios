import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, wait_exponential, retry_if_exception_type
import pybreaker

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .models import Proyecto
from .serializers import ProyectoSerializer
from django.conf import settings
from .kafka_empresa_cache import empresa_cache, start_empresa_cache_listener


start_empresa_cache_listener()


@retry(stop=stop_after_attempt(3),
       wait=wait_exponential_jitter(1, 5),
       retry=retry_if_exception_type(httpx.HTTPStatusError))
def llamar_servicio_empresa(empresa_id):
    """
    Uso se patron Retry para el servicio de Empresa
    """
    with httpx.Client(timeout=5) as client:
        r = client.get(
            f"{settings.SERVICE_EMPRESA_URL}/empresas/{empresa_id}/",
            headers={"Host": "localhost"}
        )
        r.raise_for_status()
        return r.json()


def llamar_servicio_programacion(proyecto_id):
    """
    Llamar al servicio de programacion con Circuit Breaker
    """
    with httpx.Client(timeout=5) as client:
        r = client.get(
            f"{settings.SERVICE_PROGRAMACION_URL}/programacion/completa/{proyecto_id}/",
            headers={"Host": "localhost"}
        )
        r.raise_for_status()
        return r.json()


class ProyectoListCreateView(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        empresa_id = request.data.get("empresa_id")

        # verificar si existe en Kafka cache
        if empresa_id in empresa_cache:
            print(f"[Kafka] Empresa {empresa_id} encontrada en cache")
        else:
            print(f"[Kafka] Empresa {empresa_id} no encontrada en cache, verificando por HTTP...")
            try:
                # verificar_empresa_http(empresa_id)
                llamar_servicio_empresa(empresa_id)
            except pybreaker.CircuitBreakerError:
                return Response(
                    {"error": "Servicio de empresas no disponible (Circuit Open)"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            except Exception as e:
                return Response(
                    {"error": f"No se pudo verificar la empresa: {e}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # pasa validación, crear proyecto
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Proyecto registrado con éxito", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )


class ProyectoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [AllowAny]


breaker_c = pybreaker.CircuitBreaker(fail_max=4, reset_timeout=30, name="ServiceProgramacion")


class ProyectoDetailView(APIView):

    def get(self, request, pk):
        try:
            proyecto = Proyecto.objects.get(pk=pk)
        except Proyecto.DoesNotExist:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        proyecto_data = ProyectoSerializer(proyecto).data

        # Llamada a Service A (Empresas)
        try:
            empresa_data = llamar_servicio_empresa(proyecto.empresa_id)
        except Exception as e:
            empresa_data = {"error": f"Service Empresa temporarily unavailable: {str(e)}"}

        # Llamada a Service C (Programación)
        try:
            programacion_data = breaker_c.call(llamar_servicio_programacion, proyecto.id)
        except pybreaker.CircuitBreakerError as e:
            programacion_data = {"error": f"Service Programacion unavailable (circuit open): {str(e)}"}
        except Exception as e:
            programacion_data = {"error": f"Service Programacion temporarily unavailable: {str(e)}"}

        return Response({
            "proyecto": proyecto_data,
            "empresa": empresa_data,
            "programacion-seguimiento": programacion_data
        })
