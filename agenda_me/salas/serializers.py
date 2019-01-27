from rest_framework.decorators import api_view
from rest_framework import serializers
from .models import Sala

class SalaSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Sala
        fields = ('id', 'name', 'date_created', 'date_modified')
        read_only_fields = ('id', 'date_created', 'date_modified')

    
    