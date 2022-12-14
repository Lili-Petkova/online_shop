from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Book
from .cart import Cart
from .forms import CartAddBookForm


@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    in_stock = book.stock
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        """checks the availability of the required number of books in stock"""
        if cd['quantity'] <= in_stock:
            cart.add(book=book,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        else:
            deficit = f'There are only {in_stock} books available.'
            return render(request,
                          'catalog/book_detail.html',
                          {
                              'deficit': deficit,
                              'book': book,
                              'cart_book_form': form
                          })
    return redirect('cart:cart_detail')


def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
