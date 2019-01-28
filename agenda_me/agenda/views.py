from rest_framework import generics
from .serializers import AgendaSerializer
from .models import Agenda

class CreateView(generics.ListCreateAPIView):   
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer        

    def perform_create(self, serializer):
        """Salva os dados do post e cria uma nova Agenda."""        
        serializer.save()        

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer



