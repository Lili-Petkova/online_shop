from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import generic

from catalog.forms import ContactForm
from .models import Book, Genre, Author
from cart.forms import CartAddBookForm

from .tasks import send_mail_contact


def about(request):
    return render(request, 'catalog/about.html')


def payment(request):
    return render(request, 'catalog/payment_and_delivery.html')


def contact(request):
    data = dict()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            data['form_is_valid'] = True
            #send_mail_contact.delay(text, email) селери не работает, я пока не поняла почему
            # AttributeError: 'ChannelPromise' object has no attribute '__value__'

            mes = messages.add_message(request,  messages.SUCCESS, 'Message sent')
            context = {'mes': mes}
            data['answer'] = render_to_string('catalog/includes/success.html', context, request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = ContactForm()
    context = {'form': form}
    data['html_form'] = render_to_string('catalog/includes/contact_form.html', context, request=request)
    return JsonResponse(data)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    queryset = Book.objects.filter(available=True)


class GenreList(generic.ListView):
    model = Genre
    queryset = Genre.objects.select_related()


class AuthorList(generic.ListView):
    model = Author


def books_of_genre(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    books = Book.objects.filter(genre=genre, available=True)
    paginator = Paginator(books, 1)
    page = request.GET.get('page', 1)
    try:
        page_books = paginator.page(page)
    except EmptyPage:
        raise Http404
    return render(request,
                  'catalog/books_filter.html',
                  {'genre': genre,
                   'paginator': paginator,
                   'page_books': page_books})


def books_of_author(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    books = Book.objects.filter(author=author, available=True)
    paginator = Paginator(books, 1)
    page = request.GET.get('page', 1)
    try:
        page_books = paginator.page(page)
    except EmptyPage:
        raise Http404
    return render(request,
                  'catalog/books_filter.html',
                  {'author': author,
                   'paginator': paginator,
                   'page_books': page_books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, available=True)
    cart_book_form = CartAddBookForm()
    return render(request,
                  'catalog/book_detail.html',
                  {'book': book,
                   'cart_book_form': cart_book_form})
