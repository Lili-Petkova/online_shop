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
    isbn = models.CharField(max_length=14)

    def __str__(self):
        return self.isbn
