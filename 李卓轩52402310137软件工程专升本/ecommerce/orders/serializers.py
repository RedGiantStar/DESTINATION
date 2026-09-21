from rest_framework import serializers
from orders.models import Order, OrderItem
from accounts.serializers import AddressSerializer
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'address', 'total_amount', 'status', 'items', 'created_at', 'updated_at', 'payment_time', 'shipping_time', 'completed_time']

class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(required=True)
    
    def validate_address_id(self, value):
        from accounts.models import Address
        user = self.context['request'].user
        try:
            address = Address.objects.get(pk=value, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError('地址不存在')
        return value
