from django.db import models


class Empresa(models.Model):
    razon_social = models.CharField(max_length=255)
    sigla = models.CharField(max_length=50, blank=True, null=True)
    nit = models.CharField(max_length=50, unique=True)
    representante_legal = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=512, blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        return f"{self.razon_social} ({self.nit})"
