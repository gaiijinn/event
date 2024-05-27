FROM python:3

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

# Add wait-for-it script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD /wait-for-it.sh postgres:5432 -- \
    python manage.py migrate && \
    python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(email='admin@gmail.com').exists() or User.objects.create_superuser('admin@gmail.com', 'admin')" && \
    gunicorn citymap.wsgi:application --bind 0.0.0.0:8000
