from rest_framework import generics
from .serializers import SalaSerializer
from .models import Sala

class CreateView(generics.ListCreateAPIView):   
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    def perform_create(self, serializer):
        """Salva os dados do post e cria uma nova Sala."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


   