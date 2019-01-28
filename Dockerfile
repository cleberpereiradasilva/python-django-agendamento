
FROM python:3.6
RUN mkdir /src
WORKDIR /src    
ADD requirements.txt /src/
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD ./agenda_me /src/
COPY ./docker-entrypoint.sh /src/
ENTRYPOINT ["./docker-entrypoint.sh"]

