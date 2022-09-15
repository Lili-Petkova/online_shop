from catalog.views import about, payment, contact, books_of_genre, book_detail, books_of_author

from django.urls import path

from . import views

app_name = 'catalog'
urlpatterns = [
    path('', about, name='about'),
    path('payment/', payment, name='payment'),
    path('contact/', contact, name='contact'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('genres/', views.GenreList.as_view(), name='genres_list'),
    path('authors/', views.AuthorList.as_view(), name='authors_list'),
    path('books/<genre_name>/', books_of_genre, name='books_of_genre'),
    path('books/author/<int:author_pk>/', books_of_author, name='books_of_author'),
    path('book/<int:pk>/', book_detail, name='book_detail')
]
