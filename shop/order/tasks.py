import requests, json
from celery import shared_task
from django.core.mail import send_mail

from catalog.models import Book
from order.models import Order


@shared_task
def order_created_send_mail(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.order_number)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order number is {}.'.format(order.customer, order.order_number)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent

@shared_task
def send_order_to_warehouse(title):
    data_json = json.dumps(title)
    print(data_json)
    requests.post('http://warehouse:8001/order/api/order', data_json)


@shared_task
def store_update():
    print('Starting update from warehouse api for database')
    print('Getting data from api...')

    url = 'http://localhost:8001/stock/api/book/'
    print('Clearing data...')

    response_book = requests.get(url)
    if response_book.status_code != 200:
        return
    response_data_book = response_book.json()
    while True:

        for counter, data in enumerate(response_data_book['results']):
            book, created = Book.objects.update_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    'identifier': data['identifier'],
                    "name": data['name'],
                    "author": data['author'],
                    "stock": data['amount'],
                }
            )

            if not created:
                book.name = data['name']
                book.available = data['available']
                book.author = data['author']
                book.identifier = data['identifier'],
                book.stock = data['amount'],
                book.save()

        if response_data_book['next']:
            response_data_book = requests.get(response_data_book['next']).json()
        else:
            break
    print('Database was updated from warehouse api')
