from orders.models import Order
from accounts.models import User

print('=== 数据库订单检查 ===')
print(f'总订单数: {Order.objects.count()}')
print(f'总用户数: {User.objects.count()}')

orders = Order.objects.all()
if orders.exists():
    print('\n订单列表:')
    for order in orders[:10]:
        print(f'  - 订单ID: {order.id}, 订单号: {order.order_number}, 用户: {order.user.username}, 状态: {order.status}, 总金额: {order.total_amount}')
else:
    print('\n数据库中没有订单数据')

print('\n=== 检查完成 ===')