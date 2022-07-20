from rest_framework import serializers
from .models import Agenda

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Agenda
        fields = '__all__'
        read_only_fields = ('date_created', 'date_modified', 'code')

    def create(self, validated_data):
        try:
            return Agenda.objects.create(**validated_data)
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error, code=400)

    def update(self, instance, validated_data):
        try:
            return super(AgendaSerializer, self).update(instance, validated_data)
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error, code=400)


   
        

           
    