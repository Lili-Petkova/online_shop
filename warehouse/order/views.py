from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from order.models import Order, OrderItem
from order.permissions import IsOwnerOrReadOnly
from order.serializers import GetRequestSerializer, OrderSerializer, OrderItemSerializer
from stock.models import Book


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # permission_classes = [IsOwnerOrReadOnly]


@api_view(['POST'])
def get_request(request):
    data = JSONParser().parse(request)
    serializer = GetRequestSerializer(data=data)
    if serializer.is_valid():
        queryset = Book.objects.filter(name=serializer.data['name'])
        queryset[0].delete()
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)
