import requests, json
from celery import shared_task
from django.core.mail import send_mail
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
