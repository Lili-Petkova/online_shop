from .models import Order, OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    # order_item = serializers.ReadOnlyField(source='orderitem.order')

    class Meta:
        model = OrderItem
        fields = ['order', 'book', 'quantity']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    # order = serializers.ReadOnlyField(source='order.order_number')
    items = OrderItemSerializer(source="order_item_set", many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'recipient', 'email', 'address', 'city', 'postal_code', 'created', 'status', 'items']

    def create(self, validated_data):
        valid_data = validated_data.pop('order_item_set')
        order = Order.objects.create(**validated_data)
        order_items_serializer = self.fields['order_items']
        for each in valid_data:
            each['order'] = order
        order_items_serializer.create(valid_data)
        return order, valid_data


class GetRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
