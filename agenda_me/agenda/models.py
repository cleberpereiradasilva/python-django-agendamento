from django.db import models
from salas.models import Sala

class Agenda(models.Model):    
    titulo = models.CharField(max_length=255, blank=False, unique=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, blank=True, null=True)    
    date_init = models.DateTimeField(blank=False, null=True)
    date_end = models.DateTimeField(blank=True, null=True)


    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return "{0}".format(self.titulo)
