from django.db import models
from salas.models import Sala

class Agenda(models.Model):    
    titulo = models.CharField(max_length=255, blank=False, unique=False, verbose_name="Título")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, blank=True, null=True)    
    date_init = models.DateTimeField(blank=False, null=True, verbose_name="Data/Hora de início")
    date_end = models.DateTimeField(blank=True, null=True, verbose_name="Data/Hora de término")
    created_by = models.CharField(max_length=100, null=False, blank=False, verbose_name="Criado por")
    creator_email = models.EmailField(null=False, blank=False, verbose_name="Email de quem criou")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return "{0}".format(self.titulo)

    def duplicado(self):
        date_init = self.date_init
        date_end = self.date_end
        sala = self.sala        

        '''
            checa se existe algum agendamento entre o horario de inicio fim do agendamento
            q esta tantados salvar, mesmo que duplique so sera aceito se for zero
            e tem que ser para a mesma sala claro

        '''

        agendas = Agenda.objects.all()
        if(self.id != None):
            #NO CASO DE SE UPDATE EXCLUIR O PROPRIO ID
            agendas = agendas.exclude(id=self.id)
        agendamentos = (len(agendas\
            .filter(date_init__lte=date_init)\
            .filter(date_end__gte=date_init)\
            .filter(sala_id=sala.id))
            +
            len(agendas\
            .filter(date_init__lte=date_end)\
            .filter(date_end__gte=date_end)\
            .filter(sala_id=sala.id))           
            )
        return agendamentos

    def save(self, *args, **kwargs):                
        if(self.duplicado() > 0):                 
            raise ValueError('Sala já em uso nesse dia e horário.')
        else:
            super(Agenda, self).save(*args, **kwargs)
            
