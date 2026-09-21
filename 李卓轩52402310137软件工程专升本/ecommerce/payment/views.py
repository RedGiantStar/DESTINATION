from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from payment.serializers import PaymentSerializer, CreatePaymentSerializer
from payment.models import Payment
from orders.models import Order
import uuid

class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']
        user = request.user
        
        order = Order.objects.get(pk=order_id, user=user)
        
        if hasattr(order, 'payment'):
            return Response({'error': '该订单已有支付记录'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            payment_amount=order.total_amount,
            transaction_id=f'{uuid.uuid4().hex}',
            status='pending'
        )
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentCallbackView(APIView):
    
    @transaction.atomic
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        payment_status = request.data.get('status')
        
        if not transaction_id:
            return Response({'error': '缺少交易ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return Response({'error': '支付记录不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if payment_status == 'success':
            payment.status = 'success'
            payment.paid_at = payment.updated_at
            payment.save()
            
            order = payment.order
            order.status = 'paid'
            order.payment_time = payment.paid_at
            order.save()
            
            return Response({'message': '支付成功'}, status=status.HTTP_200_OK)
        elif payment_status == 'failed':
            payment.status = 'failed'
            payment.save()
            
            return Response({'message': '支付失败'}, status=status.HTTP_200_OK)
        
        return Response({'error': '无效的支付状态'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        payments = Payment.objects.filter(order__user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
