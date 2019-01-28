from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Agenda
from salas.models import Sala
import datetime

# TESTAR CRIACAO DA AGENDA
class ModelAgendaTestCase(TestCase):
    """Testando o model Agenda."""

    def setUp(self):
        """Variaveis iniciais para o teste."""        
        self.titulo = "Reunião ABC"
        self.date_init = '2019-01-05 14:00'
        self.date_end = '2019-01-05 16:00'
        self.agenda = Agenda(
                titulo=self.titulo,
                date_init=self.date_init, 
                date_end=self.date_end
                )

        self.name = "Rua Augusta"
        self.sala = Sala(name=self.name)
        self.sala.save()
        self.agenda.sala = self.sala

    def test_model_can_create_a_agenda(self):
        """Testando se foi inserido no banco"""
        count_anterior = Agenda.objects.count()
        self.agenda.save()       
        count_atual = Agenda.objects.count()
        self.assertNotEqual(count_anterior, count_atual)
        self.assertEqual(self.agenda.sala, self.sala)

   
        
    def test_model_can_create_duplicate_agenda(self):
        """Testando se foi duplicado no banco"""
        agenda_duplicada_a = Agenda(
                titulo=self.titulo,
                date_init=self.date_init, 
                date_end=self.date_end
                )
        agenda_duplicada_b = Agenda(
                titulo=self.titulo,
                date_init=self.date_init, 
                date_end='2019-01-05 21:00'
                )
        agenda_duplicada_a.sala = self.sala
        agenda_duplicada_a.save()

        agenda_duplicada_b.sala = self.sala
        #espero que de erro
        with self.assertRaises(ValueError):
            agenda_duplicada_b.save()        
         

    def test_model_agenda_to_str(self):
        """Testando se o metodo __str__"""
        count_anterior = Agenda.objects.count()
        self.agenda.save()        
        self.assertEqual(str(self.agenda), self.titulo)


# TESTAR END POINTS
class ViewTestCase(TestCase):
    
    def setUp(self):
        """Variaveis iniciais para o teste."""
        self.sala = Sala(name="Av Paulista")
        self.sala.save()     

        self.date_init = '2019-02-05 14:00'
        self.date_end = '2019-02-05 16:00'          

        self.client = APIClient()
        self.agenda_data = {
            'titulo': 
            'Reuniao ABC', 
            'sala' : self.sala.id,
            'date_init' : self.date_init,
            'date_end' : self.date_end 
        }

        self.response = self.client.post(
            reverse('agenda'),
            self.agenda_data,
            format="json")

    def test_api_can_create_a_agenda(self):
        """Testando a criacao da agenda via post"""        
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        agenda = Agenda.objects.get()           
        self.assertEqual(agenda.sala, self.sala)

    def test_api_can_create_duplicate_agenda(self):
        """Testando a criacao da duplicada via post"""         
        
        sala = Sala(name="Av Paulista II")
        sala.save()     
        date_init = '2019-01-05 14:00'
        date_end = '2019-01-05 16:00'   
        agenda_data = {
            'titulo': 
            'Reuniao ABC', 
            'sala' : sala.id,
            'date_init' : date_init,
            'date_end' : date_end 
        }
        self.client.post(
            reverse('agenda'),
            agenda_data,
            format="json")

        date_end = '2019-01-05 18:00'  
        agenda_data['date_end'] = date_end 
        
        response = self.client.post(
            reverse('agenda'),
            agenda_data,
            format="json")

        # #espero erro 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_api_can_get_agenda(self):
        """Test the api can get a given agenda."""
        agenda = Agenda.objects.get()       
        response = self.client.get(
            reverse('details_genda',
            kwargs={'pk': agenda.id}), format="json")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, agenda) 
    
    def test_api_can_list_agendas(self):
        """Test the api can get a given agenda."""
        set_sala = {'sala': 1 , 'data_inicial' : '2019-01-01', 'data_final' : '2019-03-01'}
        response = self.client.get(
            reverse('agenda'), set_sala, format='json')        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
  
    def test_api_can_update_agenda(self):
        """Test the api can update a given agenda."""
        agenda = Agenda.objects.get()                      
        change_genda = {'titulo': 'Radial Leste'}
        res = self.client.put(
            reverse('details_genda', kwargs={'pk': agenda.id}),
            change_genda, format='json')                               
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    # def test_api_can_update_duplicate_agenda(self):
    #     """Test the api can update duplicate given agenda."""
    #     agenda = Agenda.objects.get()   
        
    #     date_init = '2019-02-05 11:00'
    #     date_end = '2019-02-05 12:00'   
    #     agenda_data = {
    #         'titulo': 
    #         'Reuniao ABC', 
    #         'sala' : self.sala.id,
    #         'date_init' : date_init,
    #         'date_end' : date_end 
    #     }

    #     res = self.client.post(
    #         reverse('agenda'),
    #         agenda_data,
    #         format="json")
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    #     agenda_data['date_end'] = '2019-02-05 15:00'
    #     res_put = self.client.put(
    #         reverse('details_genda', kwargs={'pk': 2}),
    #         agenda_data, format='json')        
    #     #print(res_put.content)                               
    #     self.assertEqual(res_put.status_code, status.HTTP_400_BAD_REQUEST)


    
    def test_api_can_delete_agenda(self):
        """Test the api can delete a agenda."""
        agenda = Agenda.objects.get()
        res = self.client.delete(
            reverse('details_genda', kwargs={'pk': agenda.id}),
            format='json',
            follow=True)        
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
