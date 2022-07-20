from django.contrib import admin

from agenda.models import Agenda

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "date_init", "date_end", "sala", "created_by")
    readonly_fields = ('code',)
