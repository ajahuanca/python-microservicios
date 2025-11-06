from django.db import models


class Proyecto(models.Model):
    empresa_id = models.IntegerField()
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.id})"

