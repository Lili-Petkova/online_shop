FROM python:3.8

COPY ./warehouse/requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./warehouse/ /app

#COPY ./docker/warehouse/runserver.sh /

#RUN chmod +x /runserver.sh

EXPOSE 8001

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8001']
#CMD ["python", "-Wd", "manage.py", "runserver"]