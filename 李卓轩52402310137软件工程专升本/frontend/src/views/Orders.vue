<template>
  <div class="orders">
    <h2 class="mb-6">订单详情</h2>

    <!-- 订单信息 -->
    <div v-if="order" class="order-info mb-6 p-4 bg-white rounded shadow">
      <div class="order-header d-flex justify-content-between align-items-center mb-4">
        <div class="order-number">订单号: {{ order.order_number }}</div>
        <div class="order-status" :class="getOrderStatusClass(order.status)">
          {{ getOrderStatusText(order.status) }}
        </div>
      </div>
      <div class="order-meta mb-4">
        <div class="row">
          <div class="col-md-3 mb-2">
            <span class="meta-label">下单时间:</span>
            <span class="meta-value">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="col-md-3 mb-2">
            <span class="meta-label">支付方式:</span>
            <span class="meta-value">{{ order.payment_method_name }}</span>
          </div>
          <div class="col-md-3 mb-2">
            <span class="meta-label">支付时间:</span>
            <span class="meta-value">{{ order.paid_at ? formatDate(order.paid_at) : '未支付' }}</span>
          </div>
          <div class="col-md-3 mb-2">
            <span class="meta-label">发货时间:</span>
            <span class="meta-value">{{ order.shipped_at ? formatDate(order.shipped_at) : '未发货' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 收货地址 -->
    <div v-if="order" class="address-section mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-3">收货地址</h3>
      <div class="address-content">
        <div class="address-info">
          <div class="name-phone">
            <span class="name font-weight-bold">{{ order.address_name }}</span>
            <span class="phone ml-3">{{ order.address_phone }}</span>
          </div>
          <div class="address-detail mt-2">
            {{ order.address_province }} {{ order.address_city }} {{ order.address_district }} {{ order.address_detail }}
          </div>
        </div>
      </div>
    </div>

    <!-- 商品信息 -->
    <div v-if="order" class="products-section mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-3">商品信息</h3>
      <div class="table-responsive">
        <table class="table table-hover">
          <thead class="thead-light">
            <tr>
              <th scope="col">商品</th>
              <th scope="col">单价</th>
              <th scope="col">数量</th>
              <th scope="col">小计</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <td>
                <div class="product-info d-flex">
                  <img :src="item.product?.image || ''" :alt="item.product?.name || ''" class="img-fluid mr-3" style="width: 80px; height: 80px; object-fit: cover;">
                  <div>
                    <h6 class="mb-1">{{ item.product?.name || '' }}</h6>
                    <p class="text-muted text-sm">{{ item.specs || '' }}</p>
                  </div>
                </div>
              </td>
              <td>¥{{ parseFloat(item.price || 0).toFixed(2) }}</td>
              <td>{{ item.quantity }}</td>
              <td>¥{{ (parseFloat(item.price || 0) * item.quantity).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 价格信息 -->
    <div v-if="order" class="price-section mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-3">价格信息</h3>
      <div class="price-details">
        <div class="row mb-2">
          <div class="col-md-6">商品总价:</div>
          <div class="col-md-6 text-right">¥{{ parseFloat(order.subtotal_amount || 0).toFixed(2) }}</div>
        </div>
        <div class="row mb-2">
          <div class="col-md-6">运费:</div>
          <div class="col-md-6 text-right">¥{{ parseFloat(order.shipping_fee || 0).toFixed(2) }}</div>
        </div>
        <div class="row mb-2">
          <div class="col-md-6">优惠:</div>
          <div class="col-md-6 text-right">-¥{{ parseFloat(order.discount_amount || 0).toFixed(2) }}</div>
        </div>
        <div class="row mb-2 font-weight-bold">
          <div class="col-md-6">实付金额:</div>
          <div class="col-md-6 text-right text-danger">¥{{ parseFloat(order.total_amount || 0).toFixed(2) }}</div>
        </div>
      </div>
    </div>

    <!-- 订单操作 -->
    <div v-if="order" class="order-actions mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-3">订单操作</h3>
      <div class="actions-content">
        <div class="d-flex flex-wrap gap-2">
          <button v-if="order.status === 'pending'" @click="payOrder(order.id)" class="btn btn-primary">
            立即支付
          </button>
          <button v-if="order.status === 'shipping'" @click="trackOrder(order.id)" class="btn btn-outline-primary">
            查看物流
          </button>
          <button v-if="order.status === 'delivered'" @click="confirmReceipt(order.id)" class="btn btn-primary">
            确认收货
          </button>
          <button v-if="order.status === 'completed'" @click="reviewOrder(order.id)" class="btn btn-outline-primary">
            评价商品
          </button>
          <button @click="contactService" class="btn btn-outline-secondary">
            联系客服
          </button>
          <button @click="printOrder(order.id)" class="btn btn-outline-secondary">
            打印订单
          </button>
        </div>
      </div>
    </div>

    <!-- 订单不存在 -->
    <div v-else-if="!loading" class="empty-order text-center py-10 bg-light rounded">
      <div class="empty-icon mb-3">
        <i class="bi bi-file-earmark"></i>
      </div>
      <h4 class="mb-2">订单不存在</h4>
      <p class="text-muted">您查看的订单不存在或已被删除</p>
      <router-link to="/profile" class="btn btn-primary mt-3">返回个人中心</router-link>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Orders',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const orderId = ref(route.params.id)
    const order = ref(null)
    const loading = ref(true)

    // 获取订单详情
    const fetchOrderDetail = async () => {
      loading.value = true
      try {
        const response = await fetch(`/api/orders/detail/${orderId.value}/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          const data = await response.json()
          // 处理订单项的图片URL
          if (data.items && Array.isArray(data.items)) {
            data.items.forEach(item => {
              if (item.product && !item.product.image) {
                // 如果商品没有图片，生成默认图片URL
                item.product.image = `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(item.product.name || 'product')}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd`
              }
            })
          }
          order.value = data
        } else {
          // 订单不存在或无权限
          order.value = null
        }
      } catch (error) {
        console.error('获取订单详情失败:', error)
        order.value = null
      } finally {
        loading.value = false
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }

    // 获取订单状态文本
    const getOrderStatusText = (status) => {
      const statusMap = {
        'pending': '待付款',
        'shipping': '待发货',
        'delivered': '待收货',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }

    // 获取订单状态样式类
    const getOrderStatusClass = (status) => {
      const classMap = {
        'pending': 'text-warning',
        'shipping': 'text-info',
        'delivered': 'text-primary',
        'completed': 'text-success',
        'cancelled': 'text-muted'
      }
      return classMap[status] || ''
    }

    // 支付订单
    const payOrder = (orderId) => {
      router.push(`/payment/${orderId}`)
    }

    // 查看物流
    const trackOrder = (orderId) => {
      // 实现查看物流功能
      console.log('查看物流:', orderId)
    }

    // 确认收货
    const confirmReceipt = async (orderId) => {
      try {
        const response = await fetch(`/api/orders/confirm/${orderId}/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          fetchOrderDetail()
        }
      } catch (error) {
        console.error('确认收货失败:', error)
      }
    }

    // 评价商品
    const reviewOrder = (orderId) => {
      // 实现评价商品功能
      console.log('评价商品:', orderId)
    }

    // 联系客服
    const contactService = () => {
      // 实现联系客服功能
      console.log('联系客服')
    }

    // 打印订单
    const printOrder = (orderId) => {
      // 实现打印订单功能
      window.print()
    }

    onMounted(() => {
      fetchOrderDetail()
    })

    return {
      orderId,
      order,
      loading,
      formatDate,
      getOrderStatusText,
      getOrderStatusClass,
      payOrder,
      trackOrder,
      confirmReceipt,
      reviewOrder,
      contactService,
      printOrder
    }
  }
}
</script>

<style scoped>
/* 订单信息样式 */
.order-info {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 地址样式 */
.address-section {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 商品样式 */
.products-section {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 价格样式 */
.price-section {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 操作样式 */
.order-actions {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .order-meta .row > div {
    flex: 0 0 100%;
    max-width: 100%;
  }
  
  .actions-content .d-flex {
    flex-direction: column;
    align-items: stretch;
  }
  
  .actions-content .btn {
    width: 100%;
  }
}
</style>