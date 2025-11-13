from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Empresa
from .serializers import EmpresaSerializer
from .kafka_producer import publish_empresa_creada_event


class EmpresaListCreateView(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        username = ''
        try:
            username = self.request.user.username
        except Exception as e:
            username = None
        empresa = serializer.save(usuario_registro=username)
        publish_empresa_creada_event(empresa)
        return Response(
            {
                "data": serializer.data,
                "message": "Registro exitoso de datos de la empresa"
            }, status=status.HTTP_201_CREATED
        )


class EmpresaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.AllowAny]
