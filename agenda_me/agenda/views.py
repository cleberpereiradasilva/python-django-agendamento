from rest_framework import generics
from .serializers import AgendaSerializer
from rest_framework.views import APIView
from .models import Agenda
from rest_framework.response import Response
from rest_framework import status



class CreateView(generics.ListCreateAPIView):   
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer        

    def perform_create(self, serializer):
        """Salva os dados do post e cria uma nova Agenda."""                        
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
    
    # def partial_update(self, serializer):     
    #     print('Atualizando..')   
    #     try: 
    #         serializer.save()             
    #     except Exception as e: 
    #         print('Erro?')           
    #         error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}            
    #         return Response(error,status=status.HTTP_400_BAD_REQUEST)
            

       
    


