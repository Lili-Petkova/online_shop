from rest_framework import serializers

from stock.models import Book, BookInstance


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['url', 'id', 'identifier', 'author', 'name', 'amount', 'created']


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['book', 'isbn', 'available']
