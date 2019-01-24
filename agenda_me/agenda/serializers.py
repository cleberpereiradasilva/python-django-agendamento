from rest_framework import serializers
from .models import Agenda


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Agenda
        fields = ('id', 'titulo', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')