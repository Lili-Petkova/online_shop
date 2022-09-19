import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.views import generic

from catalog.models import Book
from order.models import OrderItem, Order
from order.forms import OrderCreateForm
from cart.cart import Cart
from order.tasks import order_created_send_mail, send_order_to_warehouse
import random


@login_required
@transaction.atomic
def order_create(request):
    cart = Cart(request)
    customer = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_number = int(random.random() * 1000000000)
            order.customer = customer
            order.save()
            order_items = []
            book_quantity_update = []
            for item in cart:
                order_items.append(OrderItem(order=order,
                                             book=item['book'],
                                             price=item['price'],
                                             quantity=item['quantity']))
                """the number of books ordered is subtracted from the total"""
                book = item['book']
                book.stock = book.stock - item['quantity']
                book_quantity_update.append(book)
            OrderItem.objects.bulk_create(order_items)
            Book.objects.bulk_update(book_quantity_update, ['stock'])
            cart.clear()

            """Here I send an order in Json format to the warehouse, 
            I specify not the id of the book, but its identifier"""

            order_to_stock = dict()
            order_to_stock.update({
                'order_number': order.order_number,
                'recipient': order.last_name,
                'email': order.email,
                'city': order.city,
                'address': order.address,
                'postal_code': order.postal_code,
                'order_items': []
            })
            for item in order_items:
                order_to_stock['order_items'].append({
                    'book': item.book.identifier,
                    'quantity': item.quantity
                })
            send_order_to_warehouse.delay(order_to_stock)

            """Message to the user about the successful creation of the order."""
            order_created_send_mail.delay(order.id) #тоже разбираюсь с селери

            return render(request, 'order/order_success.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/order_created.html',
                  {'cart': cart, 'form': form})


class OrderList(LoginRequiredMixin, generic.ListView): # переписать так, чтобы можно было отображать книги из каждого заказа
    model = Order
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        )
