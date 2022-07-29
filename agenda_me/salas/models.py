from django.db import models

class Sala(models.Model):   
    EMPRESA_CHOICES = [
        ('Gimi', 'Gimi' ),
        ('GPB', 'GPB'),
        ('GBL', 'GBL'),
        ('GS', 'GS')
    ]


    id = models.AutoField(primary_key=True) 
    empresa = models.CharField(choices=EMPRESA_CHOICES, max_length=100, verbose_name="Empresa")
    name = models.CharField(max_length=255, blank=False, verbose_name="Nome")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
   
    def __str__(self):        
        return '{0}'.format(self.name)