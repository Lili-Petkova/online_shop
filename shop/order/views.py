from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from order.models import OrderItem, Order
from order.forms import OrderCreateForm
from cart.cart import Cart
from order.tasks import order_created_send_mail
import random


@login_required
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
            for item in cart:
                order_items.append(OrderItem(order=order,
                                             book=item['book'],
                                             price=item['price'],
                                             quantity=item['quantity']))
            OrderItem.objects.bulk_create(order_items)
            cart.clear()
            #order_created_send_mail.delay(order.id) тоже разбираюсь с селери

            """тут отправляю апи на склад и нужно указать не id книги, а его identifier"""

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
