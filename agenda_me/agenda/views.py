from rest_framework import generics
from .serializers import AgendaSerializer
from .models import Agenda
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework import status

from dotenv import load_dotenv
load_dotenv()

class CreateView(generics.ListCreateAPIView):   
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    

    def perform_create(self, serializer: AgendaSerializer):
        serializer.save()


    def get(self, request, format=None):
        agendas = Agenda.objects.all()
        sala_id = request.GET.get('sala')
        if(sala_id != None):
            agendas = agendas.filter(sala=sala_id)
        
        data_inicial = request.GET.get('data_inicial')
        data_final = request.GET.get('data_final')
        
        if(data_inicial != None and data_final != None):
            agendas = agendas.filter(date_init__gte=data_inicial)\
                .filter(date_init__lte=data_final)\
        
        serializer = AgendaSerializer(agendas, many=True)
        return Response(serializer.data)
       

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
            
    def delete(self, request: Request, *args, **kwargs):
        """
            Verifica se foi informado o código do agendamento, que foi gerado automaticamente ao ser criado.\n
            Se o código estiver correto, exclui o item.\n
            Se o código não for informado ou estiver incorreto, retorna 400 (Bad Request)
        """

        code = request.data.get('code', None)
        agenda_id = kwargs.get('pk', None)

        try:
            agenda_instance: Agenda = Agenda.objects.get(id=agenda_id)
        except Agenda.DoesNotExist:
            raise NotFound()


        if code is None:
            raise ParseError(detail={
                'detail': 'Informe o código do agendamento.',
                'code': ['Este campo é obrigatório']
            })

        try:
            if code == agenda_instance.code:
                return super().delete(request, *args, **kwargs)
            else:
                raise ValueError
        except ValueError:
            raise ParseError(detail='Código do agendamento incorreto.')
        except Exception as err:
            print('Erro ao apagar agenda:', err)
            raise ValidationError(detail={'detail': 'Erro interno no servidor.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    


