FROM python:3.8

COPY ./warehouse/requirements.txt /

RUN pip install -r requirements.txt

COPY ./warehouse/ /app

WORKDIR /app

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]