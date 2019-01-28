from rest_framework import serializers
from .models import Agenda


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Agenda
        fields = ('id', 'titulo','sala','date_init', 'date_end', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
    


    def create(self, validated_data):
        try: 
            return Agenda.objects.create(**validated_data)
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error, code=400)

    
        

           
    