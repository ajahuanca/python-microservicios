from rest_framework import serializers
from .models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'
        read_only_fields = ('id', 'fecha_registro', 'usuario_registro')
