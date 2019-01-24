from django.test import TestCase


from .models import Agenda

# TESTAR CRIACAO DA AGENDA
class ModelAgendaTestCase(TestCase):
    """Testando o model Agenda."""

    def setUp(self):
        """Variaveis iniciais para o teste."""
        """Por padrão vou usar nomes de ruas."""
        self.titulo = "Rua Augusta"
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
