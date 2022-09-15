from django.db import models


class Book(models.Model):
    identifier = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', 'author', 'amount']
        
    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey("Book", related_name='original', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.id


class Order(models.Model):
    status_choices = (
        ('processed', 'Processed'),
        ('completed', 'Completed'),
    )
    order_number = models.PositiveIntegerField()
    recipient = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=status_choices, default='processed')

    def __str__(self):
        return f'Order {self.id} is {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    book = models.OneToOneField('BookInstance', on_delete=models.CASCADE)
