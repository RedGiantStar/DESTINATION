from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from orders.serializers import OrderSerializer, CreateOrderSerializer
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from accounts.models import Address
from products.models import Product
import uuid

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        address_id = serializer.validated_data['address_id']
        user = request.user
        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': '购物车为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not cart.items.exists():
            return Response({'error': '购物车为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                return Response({'error': f'{item.product.name}库存不足'}, status=status.HTTP_400_BAD_REQUEST)
        
        order_number = f'{uuid.uuid4().hex[:10].upper()}{int(user.id)}'
        
        try:
            address = Address.objects.get(pk=address_id, user=user)
        except Address.DoesNotExist:
            return Response({'error': '地址不存在'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_amount = sum(item.subtotal for item in cart.items.all())
        
        order = Order.objects.create(
            user=user,
            address=address,
            order_number=order_number,
            total_amount=total_amount,
            status='pending'
        )
        
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                subtotal=cart_item.subtotal
            )
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        cart.items.all().delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'results': serializer.data,
            'count': len(orders)
        })

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if order.status != 'pending':
            return Response({'error': '只能取消待支付订单'}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        order.status = 'cancelled'
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if order.status != 'shipped':
            return Response({'error': '只能确认已发货的订单'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'completed'
        order.completed_time = timezone.now()
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
