<template>
  <div class="checkout">
    <h2 class="mb-6">订单结算</h2>

    <!-- 结算步骤 -->
    <div class="checkout-steps mb-6">
      <div class="step active">
        <div class="step-number">1</div>
        <div class="step-title">确认订单</div>
      </div>
      <div class="step">
        <div class="step-number">2</div>
        <div class="step-title">支付</div>
      </div>
      <div class="step">
        <div class="step-number">3</div>
        <div class="step-title">完成</div>
      </div>
    </div>

    <!-- 购物车为空或没有选中商品 -->
    <div v-if="selectedCartItems.length === 0" class="empty-checkout text-center py-10 bg-light rounded">
      <div class="empty-icon mb-3">
        <i class="bi bi-exclamation-triangle"></i>
      </div>
      <h4 class="mb-2">请先选择商品</h4>
      <p class="text-muted">请返回购物车选择要结算的商品</p>
      <router-link to="/cart" class="btn btn-primary mt-3">返回购物车</router-link>
    </div>

    <!-- 结算内容 -->
    <div v-else>
      <!-- 收货地址 -->
      <div class="address-section mb-6 p-4 bg-white rounded shadow">
        <h3 class="mb-4">收货地址</h3>
        <div class="address-list">
        <div v-for="address in addresses" :key="address.id" class="address-item mb-3">
          <div class="address-content p-3 border rounded" :class="{ 'border-primary bg-light': selectedAddressId === address.id }">
            <div class="d-flex justify-content-between">
              <div class="address-info">
                <div class="name-phone">
                  <span class="name font-weight-bold">{{ address.name }}</span>
                  <span class="phone ms-3">{{ address.phone }}</span>
                  <span v-if="address.is_default" class="default-tag ms-3">默认</span>
                </div>
                <div class="address-detail mt-2">
                  {{ address.province }} {{ address.city }} {{ address.district }} {{ address.detail }}
                </div>
              </div>
              <div class="address-actions">
                <button @click="selectAddress(address.id)" class="btn btn-sm btn-outline-primary">
                  选择
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="add-address mb-3">
          <button @click="showAddAddressForm = !showAddAddressForm" class="btn btn-outline-secondary w-100">
            <i class="bi bi-plus"></i> 添加新地址
          </button>
        </div>
      </div>

      <!-- 添加地址表单 -->
      <div v-if="showAddAddressForm" class="add-address-form p-4 border rounded mt-4">
        <h4 class="mb-3">添加新地址</h4>
        <form @submit.prevent="addAddress" class="needs-validation" novalidate>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="name" class="form-label">收件人</label>
              <input 
                v-model="newAddress.name" 
                type="text" 
                class="form-control" 
                id="name"
                required
              >
              <div class="invalid-feedback">请输入收件人姓名</div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="phone" class="form-label">手机号</label>
              <input 
                v-model="newAddress.phone" 
                type="tel" 
                class="form-control" 
                id="phone"
                required
              >
              <div class="invalid-feedback">请输入手机号</div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-4 mb-3">
              <label for="province" class="form-label">省份</label>
              <input 
                v-model="newAddress.province" 
                type="text" 
                class="form-control" 
                id="province"
                required
              >
              <div class="invalid-feedback">请输入省份</div>
            </div>
            <div class="col-md-4 mb-3">
              <label for="city" class="form-label">城市</label>
              <input 
                v-model="newAddress.city" 
                type="text" 
                class="form-control" 
                id="city"
                required
              >
              <div class="invalid-feedback">请输入城市</div>
            </div>
            <div class="col-md-4 mb-3">
              <label for="district" class="form-label">区县</label>
              <input 
                v-model="newAddress.district" 
                type="text" 
                class="form-control" 
                id="district"
                required
              >
              <div class="invalid-feedback">请输入区县</div>
            </div>
          </div>
          <div class="mb-3">
            <label for="detail" class="form-label">详细地址</label>
            <input 
              v-model="newAddress.detail" 
              type="text" 
              class="form-control" 
              id="detail"
              required
            >
            <div class="invalid-feedback">请输入详细地址</div>
          </div>
          <div class="mb-3 form-check">
            <input 
              v-model="newAddress.is_default" 
              type="checkbox" 
              class="form-check-input" 
              id="isDefault"
            >
            <label class="form-check-label" for="isDefault">设为默认地址</label>
          </div>
          <div class="form-actions">
            <button type="button" @click="showAddAddressForm = false" class="btn btn-outline-secondary me-2">
              取消
            </button>
            <button type="submit" class="btn btn-primary">
              保存地址
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 商品信息 -->
    <div class="order-section mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-4">商品信息</h3>
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
            <tr v-for="item in selectedCartItems" :key="item.id">
              <td>
                <div class="product-info d-flex">
                  <img :src="item.image_url" :alt="item.name" class="img-fluid me-3" style="width: 60px; height: 60px; object-fit: cover;">
                  <div>
                    <h6 class="mb-1">{{ item.name }}</h6>
                  </div>
                </div>
              </td>
              <td>¥{{ item.price.toFixed(2) }}</td>
              <td>{{ item.quantity }}</td>
              <td>¥{{ (item.price * item.quantity).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 支付方式 -->
    <div class="payment-section mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-4">支付方式</h3>
      <div class="payment-methods">
        <div v-for="method in paymentMethods" :key="method.id" class="payment-method mb-3">
          <div class="payment-content p-3 border rounded" :class="{ 'border-primary bg-light': selectedPaymentMethod === method.id }">
            <div class="d-flex justify-content-between">
              <div class="payment-info">
                <div class="payment-name">{{ method.name }}</div>
                <div class="payment-description text-muted text-sm">{{ method.description }}</div>
              </div>
              <div class="payment-actions">
                <button @click="selectedPaymentMethod = method.id" class="btn btn-sm btn-outline-primary">
                  选择
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 订单信息 -->
    <div class="order-info mb-6 p-4 bg-white rounded shadow">
      <h3 class="mb-4">订单信息</h3>
      <div class="order-details">
        <div class="row mb-2">
          <div class="col-md-6">商品总价:</div>
          <div class="col-md-6 text-end">¥{{ subtotal.toFixed(2) }}</div>
        </div>
        <div class="row mb-2">
          <div class="col-md-6">运费:</div>
          <div class="col-md-6 text-end">¥{{ shippingFee.toFixed(2) }}</div>
        </div>
        <div class="row mb-2">
          <div class="col-md-6">优惠:</div>
          <div class="col-md-6 text-end">-¥{{ discount.toFixed(2) }}</div>
        </div>
        <div class="row mb-2 font-weight-bold">
          <div class="col-md-6">实付金额:</div>
          <div class="col-md-6 text-end text-danger">¥{{ total.toFixed(2) }}</div>
        </div>
      </div>
      <div class="order-note mt-4">
        <label for="note" class="form-label">订单备注</label>
        <textarea v-model="orderNote" class="form-control" id="note" rows="2" placeholder="请输入订单备注"></textarea>
      </div>
    </div>

    <!-- 提交订单 -->
    <div class="submit-order mb-6">
      <div class="d-flex justify-content-between align-items-center p-4 bg-white rounded shadow">
        <div class="order-summary">
          <span>实付金额:</span>
          <span class="total-price">¥{{ total.toFixed(2) }}</span>
        </div>
        <button @click="submitOrder" class="btn btn-primary btn-lg" :disabled="!canSubmit">
          提交订单
        </button>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { useUserStore } from '../stores/user'

export default {
  name: 'Checkout',
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    const userStore = useUserStore()
    
    const addresses = ref([])
    const selectedAddressId = ref(null)
    const showAddAddressForm = ref(false)
    const newAddress = ref({
      name: '',
      phone: '',
      province: '',
      city: '',
      district: '',
      detail: '',
      is_default: false
    })
    
    const paymentMethods = ref([
      { id: 1, name: '支付宝', description: '支付宝安全支付' },
      { id: 2, name: '微信支付', description: '微信安全支付' },
      { id: 3, name: '银行卡支付', description: '银行卡安全支付' }
    ])
    const selectedPaymentMethod = ref(1)
    
    const orderNote = ref('')
    const shippingFee = ref(10)
    const discount = ref(0)
    
    const selectAddress = (addressId) => {
      selectedAddressId.value = addressId
    }
    
    // 获取用户地址
    const fetchAddresses = async () => {
      try {
        const response = await fetch('/api/accounts/addresses/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.ok) {
          addresses.value = await response.json()
          // 默认选择第一个地址
          if (addresses.value.length > 0) {
            selectedAddressId.value = addresses.value[0].id
          }
        } else if (response.status === 401 || response.status === 403) {
          // Token无效或过期，清除本地存储并提示用户重新登录
          userStore.logout()
          alert('登录已过期，请重新登录')
          router.push('/login')
        } else {
          console.error('获取地址失败:', response.status)
        }
      } catch (error) {
        console.error('获取地址失败:', error)
      }
    }

    const addAddress = async () => {
      try {
        const response = await fetch('/api/accounts/addresses/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(newAddress.value)
        })
        
        if (response.ok) {
          const newAddr = await response.json()
          addresses.value.push(newAddr)
          selectedAddressId.value = newAddr.id
          showAddAddressForm.value = false
          newAddress.value = {
            name: '',
            phone: '',
            province: '',
            city: '',
            district: '',
            detail: '',
            is_default: false
          }
        } else if (response.status === 401 || response.status === 403) {
          // Token无效或过期，清除本地存储并提示用户重新登录
          userStore.logout()
          alert('登录已过期，请重新登录')
          router.push('/login')
        } else {
          let errorMessage = '添加地址失败'
          try {
            const contentType = response.headers.get('content-type')
            if (contentType && contentType.includes('application/json')) {
              const error = await response.json()
              errorMessage = error.error || error.detail || '添加地址失败'
            } else {
              errorMessage = `服务器错误 (${response.status})`
            }
          } catch (parseError) {
            console.error('解析错误响应失败:', parseError)
          }
          alert(errorMessage)
        }
      } catch (error) {
        console.error('添加地址失败:', error)
        alert('添加地址失败，请检查网络连接后重试')
      }
    }
    
    const subtotal = computed(() => {
      return selectedCartItems.value.reduce((sum, item) => {
        return sum + item.price * item.quantity
      }, 0)
    })
    
    const total = computed(() => {
      return subtotal.value + shippingFee.value - discount.value
    })
    
    const selectedCartItems = computed(() => {
      return cartStore.items.filter(item => item.selected)
    })
    
    const canSubmit = computed(() => {
      return selectedAddressId.value && selectedPaymentMethod.value && selectedCartItems.value.length > 0
    })
    
    const submitOrder = async () => {
      if (!canSubmit.value) return
      
      try {
        const response = await fetch('/api/orders/create/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            address_id: selectedAddressId.value
          })
        })
        
        if (response.ok) {
          const order = await response.json()
          alert('订单提交成功！感谢您的购买。')
          router.push(`/order/${order.id}`)
        } else if (response.status === 401 || response.status === 403) {
          // Token无效或过期，清除本地存储并提示用户重新登录
          userStore.logout()
          alert('登录已过期，请重新登录')
          router.push('/login')
        } else {
          // 尝试解析错误响应
          let errorMessage = '提交订单失败'
          try {
            const contentType = response.headers.get('content-type')
            if (contentType && contentType.includes('application/json')) {
              const error = await response.json()
              errorMessage = error.error || error.detail || '提交订单失败'
            } else {
              // 如果不是JSON响应，可能是HTML错误页面
              const text = await response.text()
              console.error('服务器返回非JSON响应:', text.substring(0, 200))
              errorMessage = `服务器错误 (${response.status})`
            }
          } catch (parseError) {
            console.error('解析错误响应失败:', parseError)
          }
          alert(errorMessage)
        }
      } catch (error) {
        console.error('提交订单失败:', error)
        alert('提交订单失败，请检查网络连接后重试')
      }
    }
    
    onMounted(async () => {
      if (selectedCartItems.value.length === 0) {
        router.push('/cart')
        return
      }
      await fetchAddresses()
    })
    
    return {
      addresses,
      selectedAddressId,
      showAddAddressForm,
      newAddress,
      paymentMethods,
      selectedPaymentMethod,
      orderNote,
      selectedCartItems,
      subtotal,
      shippingFee,
      discount,
      total,
      canSubmit,
      selectAddress,
      addAddress,
      submitOrder
    }
  }
}
</script>

<style scoped>
.checkout-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 40px;
}

.step {
  flex: 1;
  text-align: center;
  position: relative;
}

.step::after {
  content: '';
  position: absolute;
  top: 20px;
  left: 50%;
  right: -50%;
  height: 2px;
  background-color: #dee2e6;
  z-index: 1;
}

.step:last-child::after {
  display: none;
}

.step.active {
  color: #007bff;
}

.step.active::after {
  background-color: #007bff;
}

.step-number {
  display: inline-block;
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50%;
  background-color: #dee2e6;
  margin-bottom: 10px;
  position: relative;
  z-index: 2;
}

.step.active .step-number {
  background-color: #007bff;
  color: white;
}

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

.payment-method {
  transition: all 0.3s ease;
}

.payment-method:hover {
  transform: translateY(-2px);
}

.total-price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #dc3545;
}

.empty-checkout {
  min-height: 400px;
}

.empty-icon {
  font-size: 4rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .checkout-steps {
    font-size: 0.8rem;
  }
  
  .step-number {
    width: 30px;
    height: 30px;
    line-height: 30px;
  }
  
  .step::after {
    top: 15px;
  }
}
</style>
