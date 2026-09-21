<template>
  <div class="profile">
    <h2 class="mb-6">个人中心</h2>

    <!-- 个人信息卡片 -->
    <div class="profile-card mb-6 p-4 bg-white rounded shadow">
      <div class="d-flex align-items-center">
        <div class="profile-avatar mr-4">
          <img :src="user.avatar || 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar%2C%20simple%2C%20clean&image_size=square'" :alt="user.username" class="img-fluid rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
        </div>
        <div class="profile-info">
          <h3>{{ user.username }}</h3>
          <p class="text-muted">{{ user.email }}</p>
          <div class="profile-stats mt-2">
            <span class="stat-item mr-4">订单数: {{ orderCount }}</span>
            <span class="stat-item">收藏数: {{ favoriteCount }}</span>
          </div>
        </div>
        <div class="ml-auto">
          <button @click="editProfile" class="btn btn-outline-primary">
            编辑资料
          </button>
        </div>
      </div>
    </div>

    <!-- 导航标签 -->
    <div class="profile-nav mb-6">
      <ul class="nav nav-tabs" id="profileTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active" id="orders-tab" data-bs-toggle="tab" data-bs-target="#orders" type="button" role="tab" aria-controls="orders" aria-selected="true">
            我的订单
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="addresses-tab" data-bs-toggle="tab" data-bs-target="#addresses" type="button" role="tab" aria-controls="addresses" aria-selected="false">
            收货地址
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="favorites-tab" data-bs-toggle="tab" data-bs-target="#favorites" type="button" role="tab" aria-controls="favorites" aria-selected="false">
            我的收藏
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="settings-tab" data-bs-toggle="tab" data-bs-target="#settings" type="button" role="tab" aria-controls="settings" aria-selected="false">
            账户设置
          </button>
        </li>
      </ul>
      <div class="tab-content" id="profileTabContent">
        <!-- 我的订单 -->
        <div class="tab-pane fade show active" id="orders" role="tabpanel" aria-labelledby="orders-tab">
          <div class="orders-content p-4">
            <div class="order-status-filter mb-4">
              <div class="btn-group" role="group">
                <button @click="filterOrders('all')" class="btn btn-outline-secondary" :class="{ 'btn-primary': activeOrderFilter === 'all' }">
                  全部
                </button>
                <button @click="filterOrders('pending')" class="btn btn-outline-secondary" :class="{ 'btn-primary': activeOrderFilter === 'pending' }">
                  待付款
                </button>
                <button @click="filterOrders('shipping')" class="btn btn-outline-secondary" :class="{ 'btn-primary': activeOrderFilter === 'shipping' }">
                  待发货
                </button>
                <button @click="filterOrders('delivered')" class="btn btn-outline-secondary" :class="{ 'btn-primary': activeOrderFilter === 'delivered' }">
                  待收货
                </button>
                <button @click="filterOrders('completed')" class="btn btn-outline-secondary" :class="{ 'btn-primary': activeOrderFilter === 'completed' }">
                  已完成
                </button>
              </div>
            </div>
            <div class="order-list">
              <div v-for="order in filteredOrders" :key="order.id" class="order-item mb-4 p-4 border rounded">
                <div class="order-header d-flex justify-content-between mb-3">
                  <div class="order-id">订单号: {{ order.order_number }}</div>
                  <div class="order-status" :class="getOrderStatusClass(order.status)">
                    {{ getOrderStatusText(order.status) }}
                  </div>
                </div>
                <div class="order-products mb-3">
                  <div v-for="item in order.items" :key="item.id" class="product-item d-flex mb-2">
                    <img :src="item.product?.image || ''" :alt="item.product?.name || ''" class="img-fluid mr-3" style="width: 60px; height: 60px; object-fit: cover;">
                    <div class="product-info">
                      <h6 class="mb-1">{{ item.product?.name || '' }}</h6>
                      <div class="product-price-quantity">
                        <span class="price">¥{{ parseFloat(item.price || 0).toFixed(2) }}</span>
                        <span class="quantity ml-3">x{{ item.quantity }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="order-footer d-flex justify-content-between align-items-center">
                  <div class="order-total">
                    共 {{ order.items ? order.items.length : 0 }} 件商品，合计: <span class="total-price">¥{{ parseFloat(order.total_amount || 0).toFixed(2) }}</span>
                  </div>
                  <div class="order-actions">
                    <button v-if="order.status === 'pending'" @click="payOrder(order.id)" class="btn btn-sm btn-primary mr-2">
                      立即支付
                    </button>
                    <button v-if="order.status === 'delivered'" @click="confirmReceipt(order.id)" class="btn btn-sm btn-primary mr-2">
                      确认收货
                    </button>
                    <button @click="viewOrderDetail(order.id)" class="btn btn-sm btn-outline-primary">
                      查看详情
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="filteredOrders.length === 0" class="empty-orders text-center py-6">
                <p>暂无订单</p>
                <router-link to="/" class="btn btn-outline-primary mt-3">去购物</router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 收货地址 -->
        <div class="tab-pane fade" id="addresses" role="tabpanel" aria-labelledby="addresses-tab">
          <div class="addresses-content p-4">
            <div class="address-list">
              <div v-for="address in addresses" :key="address.id" class="address-item mb-3">
                <div class="address-content p-3 border rounded">
                  <div class="d-flex justify-content-between">
                    <div class="address-info">
                      <div class="name-phone">
                        <span class="name font-weight-bold">{{ address.name }}</span>
                        <span class="phone ml-3">{{ address.phone }}</span>
                        <span v-if="address.is_default" class="default-tag ml-3">默认</span>
                      </div>
                      <div class="address-detail mt-2">
                        {{ address.province }} {{ address.city }} {{ address.district }} {{ address.detail }}
                      </div>
                    </div>
                    <div class="address-actions">
                      <button @click="editAddress(address)" class="btn btn-sm btn-outline-primary mr-2">
                        编辑
                      </button>
                      <button @click="deleteAddress(address.id)" class="btn btn-sm btn-outline-danger">
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="add-address mb-3">
                <button @click="showAddAddressForm = true" class="btn btn-outline-secondary w-100">
                  <i class="bi bi-plus"></i> 添加新地址
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 我的收藏 -->
        <div class="tab-pane fade" id="favorites" role="tabpanel" aria-labelledby="favorites-tab">
          <div class="favorites-content p-4">
            <div class="favorite-list row">
              <div v-for="product in favorites" :key="product.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
                <div class="favorite-item card h-100">
                  <div class="card-body">
                    <div class="favorite-image mb-3">
                      <router-link :to="`/product/${product.id}`">
                        <img :src="product.image_url" :alt="product.name" class="img-fluid rounded" style="height: 150px; object-fit: cover;">
                      </router-link>
                    </div>
                    <h5 class="card-title text-truncate">
                      <router-link :to="`/product/${product.id}`" class="text-decoration-none text-dark">
                        {{ product.name }}
                      </router-link>
                    </h5>
                    <div class="card-price">¥{{ product.price.toFixed(2) }}</div>
                    <div class="favorite-actions mt-3">
                      <button @click="removeFavorite(product.id)" class="btn btn-outline-danger btn-sm w-100">
                        取消收藏
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="favorites.length === 0" class="empty-favorites text-center py-6 col-12">
                <p>暂无收藏</p>
                <router-link to="/" class="btn btn-outline-primary mt-3">去购物</router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 账户设置 -->
        <div class="tab-pane fade" id="settings" role="tabpanel" aria-labelledby="settings-tab">
          <div class="settings-content p-4">
            <div class="settings-section mb-6">
              <h4 class="mb-3">账户安全</h4>
              <div class="setting-item mb-3">
                <div class="setting-label">修改密码</div>
                <div class="setting-action">
                  <button @click="changePassword" class="btn btn-outline-primary">
                    修改
                  </button>
                </div>
              </div>
              <div class="setting-item mb-3">
                <div class="setting-label">绑定手机</div>
                <div class="setting-action">
                  <span v-if="user.phone" class="mr-3">{{ user.phone }}</span>
                  <button @click="bindPhone" class="btn btn-outline-primary">
                    {{ user.phone ? '更换' : '绑定' }}
                  </button>
                </div>
              </div>
            </div>
            <div class="settings-section">
              <h4 class="mb-3">其他设置</h4>
              <div class="setting-item mb-3">
                <div class="setting-label">通知设置</div>
                <div class="setting-action">
                  <div class="form-check form-switch">
                    <input v-model="notificationSettings.order" type="checkbox" class="form-check-input" id="orderNotification">
                    <label class="form-check-label" for="orderNotification">订单通知</label>
                  </div>
                  <div class="form-check form-switch mt-2">
                    <input v-model="notificationSettings.promotion" type="checkbox" class="form-check-input" id="promotionNotification">
                    <label class="form-check-label" for="promotionNotification">促销通知</label>
                  </div>
                </div>
              </div>
              <div class="setting-item">
                <div class="setting-label">退出登录</div>
                <div class="setting-action">
                  <button @click="logout" class="btn btn-outline-danger">
                    退出登录
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

export default {
  name: 'Profile',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const user = ref({})
    const orders = ref([])
    const addresses = ref([])
    const favorites = ref([])
    const orderCount = ref(0)
    const favoriteCount = ref(0)
    const activeOrderFilter = ref('all')
    const showAddAddressForm = ref(false)
    const notificationSettings = ref({
      order: true,
      promotion: true
    })

    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/api/accounts/profile/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          user.value = await response.json()
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 获取订单列表
    const fetchOrders = async () => {
      try {
        console.log('开始获取订单列表...')
        const response = await fetch('/api/orders/list/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        console.log('订单API响应状态:', response.status)
        if (response.ok) {
          const data = await response.json()
          console.log('订单数据:', data)
          // 处理订单项的图片URL
          data.results.forEach(order => {
            if (order.items && Array.isArray(order.items)) {
              order.items.forEach(item => {
                if (item.product && !item.product.image) {
                  // 如果商品没有图片，生成默认图片URL
                  item.product.image = `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(item.product.name || 'product')}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd`
                }
              })
            }
          })
          orders.value = data.results
          orderCount.value = data.count
          console.log('订单数量:', data.count)
        } else if (response.status === 401 || response.status === 403) {
          // Token无效或过期，清除本地存储并提示用户重新登录
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          alert('登录已过期，请重新登录')
          router.push('/login')
        } else {
          console.error('获取订单失败，状态码:', response.status)
          try {
            const errorData = await response.json()
            console.error('错误信息:', errorData)
          } catch (e) {
            console.error('无法解析错误响应')
          }
        }
      } catch (error) {
        console.error('获取订单列表失败:', error)
      }
    }

    // 获取地址列表
    const fetchAddresses = async () => {
      try {
        const response = await fetch('/api/accounts/addresses/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          addresses.value = await response.json()
        }
      } catch (error) {
        console.error('获取地址列表失败:', error)
      }
    }

    // 获取收藏列表
    const fetchFavorites = async () => {
      try {
        const response = await fetch('/api/accounts/favorites/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          const data = await response.json()
          favorites.value = data.results
          favoriteCount.value = data.count
        }
      } catch (error) {
        console.error('获取收藏列表失败:', error)
      }
    }

    // 过滤订单
    const filteredOrders = computed(() => {
      if (activeOrderFilter.value === 'all') {
        return orders.value
      }
      return orders.value.filter(order => order.status === activeOrderFilter.value)
    })

    // 切换订单过滤
    const filterOrders = (status) => {
      activeOrderFilter.value = status
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

    // 查看订单详情
    const viewOrderDetail = (orderId) => {
      router.push(`/orders/${orderId}`)
    }

    // 支付订单
    const payOrder = (orderId) => {
      router.push(`/payment/${orderId}`)
    }

    // 确认收货
    const confirmReceipt = async (orderId) => {
      try {
        const response = await fetch(`/api/orders/${orderId}/confirm/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          fetchOrders()
        }
      } catch (error) {
        console.error('确认收货失败:', error)
      }
    }

    // 编辑个人资料
    const editProfile = () => {
      // 实现编辑资料功能
      console.log('编辑资料')
    }

    // 编辑地址
    const editAddress = (address) => {
      // 实现编辑地址功能
      console.log('编辑地址', address)
    }

    // 删除地址
    const deleteAddress = async (addressId) => {
      if (confirm('确定要删除此地址吗？')) {
        try {
          const response = await fetch(`/api/accounts/addresses/${addressId}/`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
          if (response.ok) {
            addresses.value = addresses.value.filter(addr => addr.id !== addressId)
          }
        } catch (error) {
          console.error('删除地址失败:', error)
        }
      }
    }

    // 移除收藏
    const removeFavorite = async (productId) => {
      try {
        const response = await fetch(`/api/accounts/favorites/${productId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          favorites.value = favorites.value.filter(fav => fav.id !== productId)
          favoriteCount.value--
        }
      } catch (error) {
        console.error('移除收藏失败:', error)
      }
    }

    // 修改密码
    const changePassword = () => {
      // 实现修改密码功能
      console.log('修改密码')
    }

    // 绑定手机
    const bindPhone = () => {
      // 实现绑定手机功能
      console.log('绑定手机')
    }

    // 退出登录
    const logout = () => {
      userStore.logout()
      router.push('/login')
    }

    onMounted(() => {
      // 检查用户是否登录
      if (!userStore.isLoggedIn) {
        router.push('/login')
        return
      }

      // 获取用户信息和相关数据
      fetchUserInfo()
      fetchOrders()
      fetchAddresses()
      fetchFavorites()
    })

    return {
      user,
      orders,
      addresses,
      favorites,
      orderCount,
      favoriteCount,
      activeOrderFilter,
      filteredOrders,
      showAddAddressForm,
      notificationSettings,
      filterOrders,
      getOrderStatusText,
      getOrderStatusClass,
      viewOrderDetail,
      payOrder,
      confirmReceipt,
      editProfile,
      editAddress,
      deleteAddress,
      removeFavorite,
      changePassword,
      bindPhone,
      logout,
      router
    }
  }
}
</script>

<style scoped>
/* 个人信息卡片样式 */
.profile-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-stats {
  font-size: 0.9rem;
}

/* 订单样式 */
.order-item {
  transition: all 0.3s ease;
}

.order-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.total-price {
  font-weight: bold;
  color: #dc3545;
}

/* 地址样式 */
.address-item {
  transition: all 0.3s ease;
}

.address-item:hover {
  transform: translateY(-2px);
}

.default-tag {
  background-color: #007bff;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* 设置样式 */
.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .profile-card {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .profile-avatar {
    margin-bottom: 20px;
  }
  
  .profile-info {
    margin-bottom: 20px;
  }
  
  .ml-auto {
    margin-left: 0 !important;
  }
}
</style>