import asyncio
import os
import time
from unidecode import unidecode
from datetime import datetime

from django.db import models
from agenda_me.utils import MailSender
from salas.models import Sala
from departamento.models import Department

class Agenda(models.Model):    
    titulo = models.CharField(max_length=255, blank=False, unique=False, verbose_name="Título")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, blank=True, null=True)    
    date_init = models.DateTimeField(blank=False, null=True, verbose_name="Data/Hora de início")
    date_end = models.DateTimeField(blank=True, null=True, verbose_name="Data/Hora de término")
    code = models.CharField(max_length=255, editable=False, blank=False, null=True, verbose_name="Código de segurança")
    created_by = models.CharField(max_length=100, null=False, blank=False, verbose_name="Criado por")
    creator_email = models.EmailField(null=False, blank=False, verbose_name="Email de quem criou")
    creator_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Departamento de quem criou")
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
    
    async def send_code_email(self, receiver_email, receiver_name, code):
        """Tenta enviar o email com o código de segurança para a pessoa que agendou"""
        mail = MailSender(os.getenv('EMAIL_SENDER_ADDRESS'), os.getenv('EMAIL_SENDER_PASSWORD'))
        try:
            mail.send_via_gmail(to=receiver_email, name=receiver_name, code=code)
            print(f'[!] Code email sended to <{receiver_email}>, from <{mail.sender_email}> at {datetime.now()} [!]')

        except Exception as e:
            print('Error sending email:', e)

    def save(self, *args, **kwargs):
        if(self.duplicado() > 0):
            raise ValueError('Sala já em uso nesse dia e horário.')
        elif (not os.getenv('EMAIL_SENDER_ADDRESS')) or (not os.getenv('EMAIL_SENDER_PASSWORD')):
            raise ValueError('Não é possível enviar um email de confirmação ao usuário.')
        else:
            # Só executa quando o dado está sendo criado no banco
            if not self.id:
                receiver_email: str = self.creator_email
                receiver_name: str = self.created_by

                # Código gerado automaticamente, deve ser enviado por email ao <receiver_email> e salvo no banco de dados.
                code = unidecode(''.join(f'{receiver_name}{time.time()}'.split()).replace('.', '').upper())
                self.code = code

                # Envia o email de forma assíncrona
                asyncio.run(self.send_code_email(receiver_email, receiver_name, code))

            super(Agenda, self).save(*args, **kwargs)

