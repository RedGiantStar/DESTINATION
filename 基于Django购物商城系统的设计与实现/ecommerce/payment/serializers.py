from rest_framework import serializers
from payment.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'payment_amount', 'transaction_id', 'status', 'created_at', 'updated_at', 'paid_at', 'refunded_at']
        read_only_fields = ['id', 'order', 'payment_amount', 'status', 'created_at', 'updated_at', 'paid_at', 'refunded_at']

class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES, required=True)
    
    def validate_order_id(self, value):
        from orders.models import Order
        user = self.context['request'].user
        try:
            order = Order.objects.get(pk=value, user=user, status='pending')
        except Order.DoesNotExist:
            raise serializers.ValidationError('订单不存在或状态不正确')
        return value
