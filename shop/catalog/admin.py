from django.contrib import admin
from catalog.models import Book, Author, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'stock', 'price', 'genre', 'available']
    list_filter = ['available', 'author', 'name']
    list_editable = ['price', 'stock', 'available']


admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Author, AuthorAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Genre, GenreAdmin)
