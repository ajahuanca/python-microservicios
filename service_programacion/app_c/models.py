from django.db import models


class Programacion(models.Model):
    proyecto_id = models.IntegerField()
    avance_fisico = models.FloatField()
    avance_financiero = models.FloatField()


class Seguimiento(models.Model):
    programacion = models.ForeignKey(Programacion, on_delete=models.CASCADE)
    observaciones = models.TextField()

