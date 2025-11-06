from rest_framework import generics, permissions
from .models import Empresa
from .serializers import EmpresaSerializer


class EmpresaListCreateView(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        username = ''
        try:
            username = self.request.user.username
        except Exception:
            username = None
        serializer.save(usuario_registro=username)


class EmpresaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]
