from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField("date of birth", null=True, blank=True)
    date_of_death = models.DateField("date of death", null=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Book(models.Model):
    identifier = models.PositiveIntegerField()
    name = models.CharField(max_length=35)
    author = models.ForeignKey("Author", related_name='book', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    genre = models.ForeignKey('Genre', related_name='book_genre', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
