from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from products.models import Product

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
            return Response({'error': '商品ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if product.stock < quantity:
            return Response({'error': '商品库存不足'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return Response({'error': '商品库存不足'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = request.data.get('quantity')
        
        if quantity is None:
            return Response({'error': '数量不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': '购物车商品不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if cart_item.product.stock < quantity:
            return Response({'error': '商品库存不足'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        try:
            cart_item = CartItem.objects.get(pk=pk, cart=cart)
            cart_item.delete()
            return Response({'message': '商品已从购物车删除'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': '购物车商品不存在'}, status=status.HTTP_404_NOT_FOUND)
