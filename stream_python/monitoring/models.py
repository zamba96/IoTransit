from django.db import models

# Create your models here.


class Registro(models.Model):
    id = models.FloatField(null=True, blank=True)
    lectura = models.FloatField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'El registro fue : $'.format(self.lectura)
