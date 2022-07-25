# Django - Agendamentos  

Esta é uma api para agendamentos de salas de reunião.  

## Cenário  

Esse sistema deve receber requisições de agendamento contendo título, sala e período de agendamento e
deve apenas reservar a sala, se a sala requisitada estiver disponível. Caso contrário, deve apresentar um erro. 
  

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
- [x] Impedir agendamentos simultâneos(Model)
- [x] Impedir agendamentos simultâneos(URL)
- [x] Uma API para listar e filtrar agendamentos por data e sala
- [x] Rodando em Docker com Postgres e gunicorn
  

## Como rodar (docker-compose) 
- Usar como path a pasta onde encontra-se o arquivo `Dockerfile`
    ```bash
        docker-compose up --build
    ``` 
- Pode haver algum problema de permissão no diretório do postgre então usar o seguinte comando:
    ```sudo chown $USER:$USER postgres_data/ -R```


## Como rodar (sem docker-compose) 
- Usar como path a pasta onde encontra-se o arquivo `manage.py`
- Configurar o banco de dados de sua preferência em ```agenda_me/agenda_me/settings.py```
- Declarar as variáveis de ambiente, conforme o arquivo `.env.example`

	```bash
		# Criar e ativar ambiente virtual
		python -m venv .venv
		.\.venv\Scripts\Activate.ps1

		# Instalar dependências
		pip install -r requirements.txt

		# Criar as tabelas necessárias para o banco de dados
		python <caminho/para/manage.py> migrate
		
		# Rodar o servidor de desenvolvimento
		python <caminho/para/manage.py> runserver

		# Caso necessário, criar um superusuário
		python <caminho/para/manage.py> createsuperuser
	``` 

## Urls

### Salas
---
- Listar todas as salas:

	- [GET] http://localhost:8000/sala/
---
- Obter dados de uma sala:

	- [GET] http://localhost:8000/sala/1
---
- Criar uma sala:

	- Campos: 
	```
		{
		  "name" : "Sala 01 Xpto"
		}
	```
	- [POST] http://localhost:8000/sala/
---
- Editar uma sala:	
	- Campos: 
	```
		{
		  "name" : "Sala 01 Xpto"
		}
	```
	- [PUT] http://localhost:8000/sala/1
---
- Remover uma sala:

	- [DELETE] http://localhost:8000/sala/1

  

### Agendas
---
- Listar todas as agendas:

	- [GET] http://localhost:8000/agenda/
---
- Obter dados de uma agenda:

	- [GET] http://localhost:8000/agenda/1
---
- Criar uma agenda:
	- Campos:
	```
		{
		  "titulo": "Reuniao ABC",
		  "sala" : 1,
		  "date_init" : "2019-01-01 14:30",
		  "date_end" : "2019-01-01 16:30"	,
			"created_by": "João",
			"creator_email": "joaozinho@gmail.com",
			"creator_department": 1
		}
	```
	- [POST] http://localhost:8000/agenda/
---
- Editar uma agenda:
	
	- Campos:
	```
		{
		  "titulo": "Reuniao ABCDeE",
		  "sala" : "1",
		  "date_init" : "2019-01-01 14:30",
		  "date_end" : "2019-01-01 16:30",
			"created_by": "João",
			"creator_email": "joaozinho@gmail.com",
			"creator_department": 1
		}
	```

	- [PUT] http://localhost:8000/agenda/1
---
- Remover uma agenda:

	- Campos: 
	```
		{
			"code" : "CODIGODOAGENDAMENTO123456"
		}
	```

	- [DELETE] http://localhost:8000/agenda/1
---
- Buscar agenda de uma sala em específica

	- [GET] http://localhost:8000/agenda/?sala=1
---
- Buscar agenda entre datas em específicas

	- [GET] http://localhost:8000/agenda/?data_inicial=2019-01-01&data_final=2019-12-12
---
- Buscar agenda entre datas em específicas e sala específica

	- [GET] http://localhost:8000/agenda/?data_inicial=2019-01-01&data_final=2019-12-12&sala=1
---



### Departamentos
---
- Listar todos os departamentos:

	- [GET] http://localhost:8000/departamento/
---
- Obter dados de um departamento:

	- [GET] http://localhost:8000/departamento/1
---
- Criar um departamento:

	- Campos:
	```
		{
		  "name": "Diretoria"
		}
	```

	- [POST] http://localhost:8000/departamento/
---
- Editar um departamento:

	- Campos:
	```
		{
			"name": "Diretoria"	
		}
	```

	- [PUT] http://localhost:8000/departamento/
---
- Remover um departamento:

	- [DELETE] http://localhost:8000/departamento/1
  
## Rodar os Testes

```bash
  python -W ignore manage.py test 
```
## Cobertura de Testes 

```bash

coverage erase; coverage run --source=salas,agenda manage.py test; coverage report
```

|Name | Stmts |Miss| Cover|
|-|-|-|-|
|agenda/models.py |24 |0 |100%
|agenda/serializers.py |19 |0 |100%
|agenda/views.py |25 |0 |100%
|salas/models.py |8 |0 |100%
|salas/serializers.py |8 |0 |100%
|salas/views.py |11 |0 |100%
|Total |95 |0 |100%   


## Outros testes

- Deixei também o arquivo do `postman` para testar se quiser: 

`Maga.postman_collection.json`

## Login
- Não fiz o login porque não pedia na documentação.


## License - MIT
  
[MIT](https://choosealicense.com/licenses/mit/)
