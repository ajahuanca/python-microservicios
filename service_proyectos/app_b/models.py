from django.db import models


class Proyecto(models.Model):
    empresa_id = models.IntegerField()
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)

