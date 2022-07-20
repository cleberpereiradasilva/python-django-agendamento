from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
