from copy import copy
import os
import re
import time
from typing import Union
from unidecode import unidecode
from datetime import datetime

from django.db import models
from agenda.models.agenda_base import AgendaBase
from agenda.models.periodic_agenda import PeriodicAgenda
from agenda_me.utils import MailSender
from salas.models import Sala
from departamento.models import Department


class Agenda(AgendaBase):
    date_init = models.DateTimeField(blank=False, null=True, verbose_name="Data/Hora de início")
    date_end = models.DateTimeField(blank=True, null=True, verbose_name="Data/Hora de término")
    must_repeat = models.BooleanField(default=False, verbose_name="Reunião se repete?", blank=True)

    def send_code_email(self, receiver_email, receiver_name, code):
        """Tenta enviar o email com o código de segurança para a pessoa que agendou"""

        mail = MailSender(os.getenv('EMAIL_SENDER_ADDRESS'), os.getenv('EMAIL_SENDER_PASSWORD'), sender_email_alias='Reuniao GIMI <reuniao@gimi.com.br>')
        mail.send_via_outlook(to=receiver_email, name=receiver_name, code=code)
        print(f'[!] Code email sended to <{receiver_email}>, from <{mail.sender_email}> at {datetime.now()} [!]')

    def save(self, *args, **kwargs):
        code = kwargs.pop('code', None)

        if(self.duplicado(Agenda) > 0):
            raise ValueError('Sala já em uso nesse dia e horário.')
        elif (not os.getenv('EMAIL_SENDER_ADDRESS')) or (not os.getenv('EMAIL_SENDER_PASSWORD')):
            raise ValueError('Não foi possível enviar um email de confirmação ao usuário.')
        else:
            # Só executar quando o dado está sendo criado no banco
            if not self.id:
                receiver_email: str = self.creator_email
                receiver_name: str = self.created_by

                # Código gerado automaticamente e salvo na instancia.
                code = code or self.generate_code(receiver_name=receiver_name)
                self.code = code

                # Envia o email com o <code> ao <receiver_email> 
                try:
                    self.send_code_email(receiver_email, receiver_name, code)
                except Exception as e:
                    print('Error sending email:', e)
                    raise ConnectionError('Erro de conexão ao enviar o email de confirmação. Tente novamente.')

            # Só executar quando for editar
            if self.id:
                pass
                
            super(Agenda, self).save(*args, **kwargs)
