from typing import Callable, Union
from rest_framework import generics, views, viewsets
from agenda.models.periodic_agenda import PeriodicAgenda
from copy import deepcopy

from .serializers import AgendaNoCodeFieldSerializer, AgendaSerializer, PeriodicAgendaSerializer
from .models import Agenda
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ParseError, NotFound, ValidationError, NotAcceptable
from rest_framework import status

from django.db.models.query import QuerySet

from datetime import datetime, timedelta, date, time
from dotenv import load_dotenv
load_dotenv()


class CreateView(generics.ListCreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def post(self, request: Request, *args, **kwargs):
        must_repeat: Union[bool, None] = request.data.get('must_repeat', None)
        must_repeat = True if must_repeat == 'true' else False
        repeat_weekday: Union[list[int], None] = request.data.getlist('repeat_weekday', None)

        change_dict_keyname: Callable[[dict, str, str]] = lambda d, old_k, new_k: {new_k if k == old_k else k:v for k,v in d.items()}

        # valida os campos no body da request
        serializer = AgendaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = deepcopy(serializer.data)
        serializer_data = change_dict_keyname(old_k='sala', new_k='sala_id', d=serializer_data)
        serializer_data = change_dict_keyname(old_k='creator_department', new_k='creator_department_id', d=serializer_data)
        headers = self.get_success_headers(serializer.data)

        # cria a instância da agenda (sem salvar no banco)
        agenda = Agenda(**serializer_data)
        periodic_agenda = None

        response_data = serializer_data

        if must_repeat is True:
            if (repeat_weekday is None) or (str(None) in repeat_weekday):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'message': 'Informe os dias da semana que a reunião irá se repetir.',
                    'repeat_weekday': ['Este campo é obrigatório.']
                })
            
            from_datetime_to_time = lambda datetime: datetime.split('T')[1].replace('Z', '')

            agenda_data = deepcopy(agenda.__dict__)
            agenda_data.pop('_state', None)
            agenda_data.pop('must_repeat', None)
            agenda_data.update({
                'time_init': from_datetime_to_time(agenda_data.pop('date_init', None)),
                'time_end': from_datetime_to_time(agenda_data.pop('date_end', None)),
                'repeat_weekday': repeat_weekday,
                'code': agenda_data.get('code', None)
            })
            agenda_data.pop('id', None)
            agenda_data = {'sala_id' if k == 'sala' else k:v for k,v in agenda_data.items()}
            agenda_data = {'creator_department_id' if k == 'creator_department' else k:v for k,v in agenda_data.items()}
            
            periodic_agenda = PeriodicAgenda(**agenda_data)
            serializer = PeriodicAgendaSerializer(periodic_agenda)
            response_data.update({
                'detail': {
                    'message': 'Agenda periódica criada.',
                    'repeat_weekday': serializer.data.get('repeat_weekday')
                },
            })

        try:
            agenda.save()
            if periodic_agenda is not None:
                periodic_agenda.save(code=agenda.code)
        except Exception as e:
            raise NotAcceptable(e)

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

            
    def get(self, request: Request, format=None):
        agendas = Agenda.objects.all()
        sala_id = request.GET.get('sala')
        if(sala_id != None):
            agendas = agendas.filter(sala=sala_id)
        
        data_inicial = request.GET.get('data_inicial')
        data_final = request.GET.get('data_final')
        
        if(data_inicial != None and data_final != None):
            agendas = agendas.filter(date_init__gte=data_inicial)\
                .filter(date_init__lte=data_final)\
        
        serializer = AgendaSerializer(agendas, many=True)
        return Response(serializer.data)
       

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    # def get_serializer_class(self):
    #     if self.request.user.is_superuser:
    #         return AgendaSerializer
    #     else:
    #         return AgendaNoCodeFieldSerializer
            
    def delete(self, request: Request, *args, **kwargs):
        """
            Verifica se foi informado o código do agendamento, que foi gerado automaticamente ao ser criado.\n
            Se o código estiver correto, exclui o item.\n
            Se o código não for informado ou estiver incorreto, retorna 400 (Bad Request)
        """

        code = request.data.get('code', None)
        must_repeat = request.data.get('must_repeat', None)
        agenda_id = kwargs.get('pk', None)

        try:
            agenda_instance: Agenda = Agenda.objects.get(id=agenda_id)
        except Agenda.DoesNotExist:
            raise NotFound()


        if code is None:
            raise ParseError(detail={
                'detail': 'Informe o código do agendamento.',
                'code': ['Este campo é obrigatório']
            })

        try:
            if code == agenda_instance.code:
                super().delete(request, *args, **kwargs)
                response_data = {}

                if must_repeat is False:
                    # apaga a PeriodicAgenda correspondente à agenda em <agenda_instance>
                    periodic_item: Union[PeriodicAgenda, None] = PeriodicAgenda.objects.filter(code=agenda_instance.code).first()
                    if periodic_item is not None:
                        periodic_item.delete()
                        response_data['message'] = 'Agendamento periódico cancelado.'
                    else:
                        response_data['message'] = 'Agendamento periódico não encontrado.'

                    # desativa a repetição das outras agendas iguais
                    other_same_agendas: QuerySet[Agenda] = Agenda.objects.filter(code=agenda_instance.code)
                    for agenda in other_same_agendas:
                        agenda.must_repeat = False
                        agenda.save()

                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                raise ValueError
        except ValueError:
            raise ParseError(detail='Código do agendamento incorreto.')
        except Exception as err:
            print('Erro ao apagar agenda:', err)
            raise ValidationError(detail={'detail': 'Erro interno no servidor.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshAgendaView(views.APIView):
    def _date_for_this_weekday(self, day: int) -> date:
        """Retorna uma data <date> desta semana, que corresponde a data no dia da semana <day>"""

        today = date.today()
        weekday = today.weekday()
        return today + timedelta(days = day - weekday)
    
    def _check_periodic_items(self, request: Request, periodic_items: QuerySet[PeriodicAgenda]):
        """
            Verifica se há reuniões (que já ocorreram) que devem ocorrer novamente.\n
            Caso haja, cria uma cópia de cada reunião para ocorrer (no(s) dia(s) da semana
            especificado(s)) durante a semana atual.\n
            .\n
            Retorna as Agendas criadas ou None.
        """
        
        # agendas que já terminaram e que são periódicas
        agendas = periodic_items
        created_this_week: list[Agenda] = []

        # todas as salas
        # salas: QuerySet[Sala] = Sala.objects.all()

        sala_id = request.GET.get('sala')
        if sala_id is not None:
            # reuniões periódicas na sala específica
            agendas: QuerySet[PeriodicAgenda] = agendas.filter(sala=sala_id)
            for agenda in agendas:
                repeat_weekdays: list[str] = list(agenda.repeat_weekday)
                print(repeat_weekdays)
                for weekday in repeat_weekdays:
                    print(f'Verificando agenda "{agenda}", dia {weekday}')
                    this_weekday_date: date = self._date_for_this_weekday(int(weekday))

                    new_date_init = datetime.combine(this_weekday_date, agenda.time_init)
                    new_date_end = datetime.combine(this_weekday_date, agenda.time_end)

                    agenda_fields = {
                        'titulo': agenda.titulo,
                        'sala': agenda.sala,
                        'created_by': agenda.created_by,
                        'creator_email': agenda.creator_email,
                        'creator_department': agenda.creator_department,

                        # datas desta semana, no mesmo dia da semana e horário.
                        'date_init': new_date_init,
                        'date_end': new_date_end,
                    }


                    today = date.today()
                    time_first = time(0, 0, 0, 0)
                    time_last = time(23, 59, 59, 0)
                    today_00_00 = datetime.combine(today, time_first)
                    today_23_59 = datetime.combine(today, time_last)
                    today_weekday = today.weekday()

                    this_monday = today_00_00 + timedelta(days = 0 - today_weekday) # segunda-feira, 00h00
                    this_sunday = today_23_59 + timedelta(days = 6 - today_weekday) # domingo, 23h59

                    # Se já houver uma reunião nesta semana com as mesmas informações, não cria outra.
                    already_created_on_this_week = bool(Agenda.objects.filter(date_end__gte=this_monday, date_end__lte=this_sunday, **agenda_fields))
                    # Agenda.objects.get_or_create()

                    if (already_created_on_this_week is True):
                        print(f'Agenda "{agenda}" no dia {weekday} já existe nessa semana.\n')
                    else:
                        new_agenda = Agenda(**agenda_fields)
                        print(f'Agenda "{agenda}" no dia {weekday} ainda não existe nessa semana, criando uma cópia...')
                        print(f'Agenda nova criada: "{new_agenda}" | inicio as: {new_agenda.date_init} | ate: {new_agenda.date_end} | email: {new_agenda.creator_email}\n')
                        new_agenda.save(code=agenda.code)
                        created_this_week.append(new_agenda)
        
        return created_this_week if len(created_this_week) > 0 else None

    def get(self, request: Request):
        periodic_items = PeriodicAgenda.objects.all()
        if bool(periodic_items) is False:
            return Response({
                'message': 'Não há agendas periódicas.'
            })

        try:
            created_items = self._check_periodic_items(request, periodic_items)
            return Response(
                {
                    'message': 'Agenda da semana atualizada com sucesso.',
                    'agendas_criadas': [{
                        'titulo': f'{item.titulo}',
                        'date_init': f'{item.date_init}',
                        'date_end': f'{item.date_end}',
                    } for item in created_items] if (created_items is not None ) else 'Nenhuma agenda precisou ser criada.'
                },
                status=status.HTTP_201_CREATED if (created_items is not None) else status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            raise ValidationError(detail={'message': 'Erro ao atualizar agenda desta semana.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PeriodicAgendaViewSet(viewsets.ModelViewSet):
    queryset = PeriodicAgenda.objects.all()
    serializer_class = PeriodicAgendaSerializer
