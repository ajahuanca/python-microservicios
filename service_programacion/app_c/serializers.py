from rest_framework import serializers
from .models import ProgramacionFisico, ProgramacionFinanciera, Seguimiento


class ProgramacionFisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionFisico
        fields = '__all__'


class ProgramacionFinancieraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionFinanciera
        fields = '__all__'


class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = '__all__'
