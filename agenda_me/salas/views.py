from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import SalaSerializer
from .models import Sala

class CreateView(ListCreateAPIView):   
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    def perform_create(self, serializer):
        """Salva os dados do post e cria uma nova Sala."""
        serializer.save()

class DetailsView(RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

    

   