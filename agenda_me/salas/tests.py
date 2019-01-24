from django.test import TestCase
from .models import Sala


class ModelSalaTestCase(TestCase):
    """Testando o model Sala."""

    def setUp(self):
        """Variaveis iniciais para o teste."""
        """Por padrão vou usar nomes de ruas."""
        self.name = "Rua Augusta"
        self.sala = Sala(name=self.name)

    def test_model_can_create_a_sala(self):
        """Testando se foi inserido no banco"""
        count_anterior = Sala.objects.count()
        self.sala.save()
        count_atual = Sala.objects.count()
        self.assertNotEqual(count_anterior, count_atual)
