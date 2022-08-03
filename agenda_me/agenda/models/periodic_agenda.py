from functools import reduce
import operator
from typing import Callable
from multiselectfield import MultiSelectField
from django.db import models

from agenda.models.agenda_base import AgendaBase

class Weekdays():
    NONE = None
    SEGUNDA_FEIRA = 0
    TERCA_FEIRA = 1
    QUARTA_FEIRA = 2
    QUINTA_FEIRA = 3
    SEXTA_FEIRA = 4
    SABADO = 5


class PeriodicAgenda(AgendaBase):
    WEEKDAY_CHOICES = (
        (Weekdays.NONE, 'nenhum'),
        (Weekdays.SEGUNDA_FEIRA, 'segunda-feira'),
        (Weekdays.TERCA_FEIRA, 'terça-feira'),
        (Weekdays.QUARTA_FEIRA, 'quarta-feira'),
        (Weekdays.QUINTA_FEIRA, 'quinta-feira'),
        (Weekdays.SEXTA_FEIRA, 'sexta-feira'),
        (Weekdays.SABADO, 'sábado')
    )

    repeat_weekday = MultiSelectField(choices=WEEKDAY_CHOICES, max_choices=6, max_length=11, null=True, blank=True, verbose_name="Dias que se repete")
    time_init = models.TimeField(null=False, blank=False, verbose_name="Hora de início")
    time_end = models.TimeField(null=False, blank=False, verbose_name="Hora de término")
    
    def duplicado(self):
        """
            Checa se existe algum agendamento periódico que já ocorre no mesmo
            dia da semana e no mesmo horário.
        """

        time_init = self.time_init
        time_end = self.time_end
        sala = self.sala    
        repeat_weekday = list(self.repeat_weekday)    

        agendas = PeriodicAgenda.objects.all()

        or_query: Callable[[list[int]]] = lambda weekdays: reduce(operator.or_, (models.Q(repeat_weekday__icontains=weekday) for weekday in weekdays))

        if(self.id != None):
            #NO CASO DE SE UPDATE EXCLUIR O PROPRIO ID
            agendas = agendas.exclude(id=self.id)
        agendamentos_same_time = (len(agendas\
            .filter(time_init__lte=time_init)\
            .filter(time_end__gte=time_init)\
            .filter(sala_id=sala.id))
            +
            len(agendas\
            .filter(time_init__lte=time_end)\
            .filter(time_end__gte=time_end)\
            .filter(sala_id=sala.id))
            )
        agendamentos_same_weekday = len(agendas.filter(or_query(repeat_weekday)).filter(sala_id=sala.id))
    
        return bool(agendamentos_same_time and agendamentos_same_weekday)

    def save(self, *args, **kwargs):
        print('duplicado:', self.duplicado())
        if(self.duplicado() is True):
            raise ValueError('Horário não disponível. Horário já agendado semanalmente.')
        else:
            code = kwargs.pop('code')
            self.code = code
            super(PeriodicAgenda, self).save(*args, **kwargs)