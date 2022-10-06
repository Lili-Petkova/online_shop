
FROM python:3.8

COPY ./shop/requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./shop/ .

COPY ./docker/shop/runserver.sh /app

RUN chmod +x runserver.sh

EXPOSE 8000

CMD ["runserver.sh"]
#CMD ["python", "-Wd", "manage.py", "runserver"]