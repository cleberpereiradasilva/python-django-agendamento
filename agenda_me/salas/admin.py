from django.contrib import admin
from salas.models import Sala

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links =  ("id", "name")