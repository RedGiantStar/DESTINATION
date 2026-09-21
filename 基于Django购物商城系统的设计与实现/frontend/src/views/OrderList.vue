<template>
  <div class="order-list">
    <h2 class="mb-6">我的订单</h2>

    <!-- 订单状态筛选 -->
    <div class="order-filter mb-6">
      <div class="filter-tabs">
        <button 
          v-for="status in orderStatuses" 
          :key="status.value"
          @click="selectedStatus = status.value"
          :class="['filter-tab', { active: selectedStatus === status.value }]"
        >
          {{ status.label }}
        </button>
      </div>
    </div>

    <!-- 订单列表 -->
    <div v-if="orders.length > 0" class="orders-container">
      <div v-for="order in filteredOrders" :key="order.id" class="order-item mb-6 p-4 bg-white rounded shadow">
        <!-- 订单头部 -->
        <div class="order-header d-flex justify-content-between align-items-center mb-4">
          <div class="order-number">订单号: {{ order.order_number }}</div>
          <div class="order-status" :class="getOrderStatusClass(order.status)">
            {{ getOrderStatusText(order.status) }}
          </div>
        </div>

        <!-- 订单商品 -->
        <div class="order-products mb-4">
          <div v-for="item in order.items" :key="item.id" class="product-item d-flex mb-3 pb-3 border-bottom">
            <img :src="`https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(item.product.name)}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd`" :alt="item.product.name" class="product-image">
            <div class="product-info flex-grow-1 ms-3">
              <h6 class="product-name">{{ item.product.name }}</h6>
              <div class="product-price-quantity d-flex justify-content-between">
                <span class="price">¥{{ parseFloat(item.price).toFixed(2) }}</span>
                <span class="quantity">x{{ item.quantity }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 订单金额 -->
        <div class="order-amount mb-4 text-right">
          <span class="total-label">共{{ order.items.length }}件商品，总计:</span>
          <span class="total-price">¥{{ parseFloat(order.total_amount).toFixed(2) }}</span>
        </div>

        <!-- 订单操作 -->
        <div class="order-actions d-flex flex-wrap gap-2 justify-content-end">
          <button v-if="order.status === 'pending'" @click="cancelOrder(order.id)" class="btn btn-outline-danger">
            取消订单
          </button>
          <button v-if="order.status === 'pending'" @click="payOrder(order.id)" class="btn btn-primary">
            立即支付
          </button>
          <button v-if="order.status === 'paid'" @click="viewOrder(order.id)" class="btn btn-outline-primary">
            查看详情
          </button>
          <button v-if="order.status === 'shipped'" @click="confirmReceipt(order.id)" class="btn btn-primary">
            确认收货
          </button>
          <button v-if="order.status === 'completed'" @click="viewOrder(order.id)" class="btn btn-outline-primary">
            查看详情
          </button>
          <button v-if="order.status === 'cancelled'" @click="viewOrder(order.id)" class="btn btn-outline-secondary">
            查看详情
          </button>
        </div>
      </div>
    </div>

    <!-- 空订单状态 -->
    <div v-else-if="!loading" class="empty-orders text-center py-10 bg-light rounded">
      <div class="empty-icon mb-3">
        <i class="bi bi-file-earmark-text"></i>
      </div>
      <h4 class="mb-2">暂无订单</h4>
      <p class="text-muted">您还没有订单记录</p>
      <router-link to="/" class="btn btn-primary mt-3">去购物</router-link>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading text-center py-10 bg-light rounded">
      <div class="spinner-border" role="status">
        <span class="sr-only">加载中...</span>
      </div>
      <p class="mt-3">加载中，请稍候...</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'OrderList',
  setup() {
    const router = useRouter()
    const orders = ref([])
    const loading = ref(true)
    const selectedStatus = ref('all')

    // 订单状态选项
    const orderStatuses = [
      { value: 'all', label: '全部' },
      { value: 'pending', label: '待付款' },
      { value: 'paid', label: '待发货' },
      { value: 'shipped', label: '待收货' },
      { value: 'completed', label: '已完成' },
      { value: 'cancelled', label: '已取消' }
    ]

    // 获取订单列表
    const fetchOrders = async () => {
      loading.value = true
      try {
        const response = await fetch('/api/orders/list/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          orders.value = await response.json()
        } else {
          console.error('获取订单列表失败')
        }
      } catch (error) {
        console.error('获取订单列表失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 筛选订单
    const filteredOrders = computed(() => {
      if (selectedStatus.value === 'all') {
        return orders.value
      }
      return orders.value.filter(order => order.status === selectedStatus.value)
    })

    // 获取订单状态文本
    const getOrderStatusText = (status) => {
      const statusMap = {
        'pending': '待付款',
        'paid': '待发货',
        'shipped': '待收货',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }

    // 获取订单状态样式类
    const getOrderStatusClass = (status) => {
      const classMap = {
        'pending': 'text-warning',
        'paid': 'text-info',
        'shipped': 'text-primary',
        'completed': 'text-success',
        'cancelled': 'text-muted'
      }
      return classMap[status] || ''
    }

    // 查看订单详情
    const viewOrder = (orderId) => {
      router.push(`/order/${orderId}`)
    }

    // 支付订单
    const payOrder = (orderId) => {
      router.push(`/payment/${orderId}`)
    }

    // 取消订单
    const cancelOrder = async (orderId) => {
      if (confirm('确定要取消这个订单吗？')) {
        try {
          const response = await fetch(`/api/orders/${orderId}/cancel/`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
          if (response.ok) {
            alert('订单已取消')
            fetchOrders()
          } else {
            const error = await response.json()
            alert(error.error || '取消订单失败')
          }
        } catch (error) {
          console.error('取消订单失败:', error)
          alert('取消订单失败，请重试')
        }
      }
    }

    // 确认收货
    const confirmReceipt = async (orderId) => {
      if (confirm('确认收货吗？')) {
        try {
          const response = await fetch(`/api/orders/${orderId}/confirm/`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
          if (response.ok) {
            alert('确认收货成功')
            fetchOrders()
          } else {
            const error = await response.json()
            alert(error.error || '确认收货失败')
          }
        } catch (error) {
          console.error('确认收货失败:', error)
          alert('确认收货失败，请重试')
        }
      }
    }

    onMounted(() => {
      fetchOrders()
    })

    return {
      orders,
      loading,
      selectedStatus,
      orderStatuses,
      filteredOrders,
      getOrderStatusText,
      getOrderStatusClass,
      viewOrder,
      payOrder,
      cancelOrder,
      confirmReceipt
    }
  }
}
</script>

<style scoped>
.order-filter {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-tabs {
  display: flex;
  gap: 1rem;
}

.filter-tab {
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-tab:hover {
  border-color: #007bff;
  color: #007bff;
}

.filter-tab.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.order-item {
  transition: all 0.3s ease;
}

.order-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.product-name {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.price {
  color: #dc3545;
  font-weight: bold;
}

.total-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #dc3545;
}

.empty-orders {
  min-height: 400px;
}

.empty-icon {
  font-size: 4rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .filter-tabs {
    flex-wrap: wrap;
  }
  
  .filter-tab {
    flex: 1;
    min-width: 80px;
    text-align: center;
  }
  
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .order-actions {
    justify-content: center;
  }
  
  .order-actions .btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>
