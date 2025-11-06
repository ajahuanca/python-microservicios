from django.db import models


class ProgramacionFisico(models.Model):
    proyecto_id = models.IntegerField()
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    avance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)


class ProgramacionFinanciera(models.Model):
    proyecto_id = models.IntegerField()
    monto_programado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_ejecutado = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class Seguimiento(models.Model):
    proyecto_id = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField()
