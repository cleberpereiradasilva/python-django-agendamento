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

 - [ ] Uma API para criar, editar e remover salas de reuniões
 - [ ] Uma API para criar, editar e remover agendamentos
 - [ ] Uma API para listar e filtrar agendamentos por data e sala

 ## Como rodar

```bash
pip install -r requirements.txt 
python manage.py runserver
```
 

## License - MIT

[MIT](https://choosealicense.com/licenses/mit/)