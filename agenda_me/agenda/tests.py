from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Agenda

# TESTAR CRIACAO DA AGENDA
class ModelAgendaTestCase(TestCase):
    """Testando o model Agenda."""

    def setUp(self):
        """Variaveis iniciais para o teste."""        
        self.titulo = "Reunião ABC"
        self.agenda = Agenda(titulo=self.titulo)

    def test_model_can_create_a_agenda(self):
        """Testando se foi inserido no banco"""
        count_anterior = Agenda.objects.count()
        self.agenda.save()
        count_atual = Agenda.objects.count()
        self.assertNotEqual(count_anterior, count_atual)

    def test_model_agenda_to_str(self):
        """Testando se o metodo __str__"""
        count_anterior = Agenda.objects.count()
        self.agenda.save()        
        self.assertEqual(str(self.agenda), self.titulo)


# TESTAR END POINTS
class ViewTestCase(TestCase):
    
    def setUp(self):
        """Variaveis iniciais para o teste."""
        self.client = APIClient()
        self.agenda_data = {'titulo': 'Reuniao ABC'}
        self.response = self.client.post(
            reverse('create_agenda'),
            self.agenda_data,
            format="json")

    def test_api_can_create_a_agenda(self):
        """Testando a criacao da agenda via post"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
