from django.db import models

from stock.models import BookInstance


class Order(models.Model):
    status_choices = (
        ('processed', 'Processed'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )
    order_number = models.PositiveIntegerField()
    recipient = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=10, choices=status_choices, default='processed')

    def __str__(self):
        return f'Order {self.order_number} is {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    book = models.ManyToManyField(BookInstance, related_name='instance_in_order')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.book} is {self.quantity}'

