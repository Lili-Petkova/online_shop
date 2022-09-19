from django.contrib import admin

from .models import Book, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    fk_name = "book"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['identifier', 'name', 'author', 'amount', 'created']
    list_filter = ['identifier', 'name']
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookItemAdmin(admin.ModelAdmin):
    fields = ['book', 'order', 'isbn', 'available']
    list_filter = ['isbn']
