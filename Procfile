release: python agenda_me/manage.py migrate
web: gunicorn --chdir agenda_me agenda_me.wsgi --log-file -