# Django - Agendamentos

Esta é uma api para agendamentos de salas de reunião.

## Cenário

Esse sistema deve receber requisições de agendamento contendo título, sala e período de agendamento e
deve apenas reservar a sala, se a sala requisitada estiver disponível. Caso contrário, deve apresentar um
erro.


## Requisitos

 - Disponibilizar o projeto em algum repositório
 - O Webservice deve seguir os princípios REST
 - Salvar as informações necessárias em um banco de dados (relacional ou não), de sua escolha
 - Testes automatizados com informação da cobertura de testes
 - Gerar logs das ações
 - Documentar como rodar o projeto

## Entregáveis

 - [x] Uma API para criar, editar e remover salas de reuniões
 - [x] Uma API para criar, editar e remover agendamentos
 - [ ] Uma API para listar e filtrar agendamentos por data e sala

 ## Como rodar

```bash
pip install -r requirements.txt 
python manage.py runserver
```

## Cobertura de Testes


```bash
coverage erase; coverage run --source=salas,agenda manage.py test; coverage report


```
|Name                    | Stmts |Miss| Cover|
|-|-|-|-|
|agenda/models.py           |11      |0   |100%
|agenda/serializers.py       |7      |0   |100%
|agenda/views.py            |13      |0   |100%
|salas/models.py             |8      |0   |100%
|salas/serializers.py        |8      |0   |100%
|salas/views.py             |11      |0   |100%
|Total                      |58      |0   |100%
 

## License - MIT

[MIT](https://choosealicense.com/licenses/mit/)