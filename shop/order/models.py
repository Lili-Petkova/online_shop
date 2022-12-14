from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Book


User = get_user_model()


class Order(models.Model):
    status_choices = (
        ('failed', 'Failed'),
        ('processed', 'Processed'),
        ('completed', 'Completed'),
    )
    order_number = models.PositiveIntegerField()
    customer = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.CharField(max_length=10, choices=status_choices, default='processed')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='order_books', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
