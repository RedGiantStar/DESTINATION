<template>
  <div class="cart">
    <h2 class="mb-6">购物车</h2>

    <!-- 购物车为空 -->
    <div v-if="cartStore.items.length === 0" class="empty-cart text-center py-10 bg-light rounded">
      <div class="empty-icon mb-3">
        <i class="bi bi-cart"></i>
      </div>
      <h4 class="mb-2">购物车为空</h4>
      <p class="text-muted">快去挑选心仪的商品吧</p>
      <router-link to="/" class="btn btn-primary mt-3">去购物</router-link>
    </div>

    <!-- 购物车商品列表 -->
    <div v-else class="cart-items">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead class="thead-light">
            <tr>
              <th scope="col">
                <div class="form-check">
                  <input 
                    v-model="selectAll" 
                    type="checkbox" 
                    class="form-check-input" 
                    id="selectAll"
                    @change="handleSelectAll"
                  >
                  <label class="form-check-label" for="selectAll">全选</label>
                </div>
              </th>
              <th scope="col">商品信息</th>
              <th scope="col">单价</th>
              <th scope="col">数量</th>
              <th scope="col">小计</th>
              <th scope="col">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cartStore.items" :key="item.id">
              <td>
                <div class="form-check">
                  <input 
                    v-model="item.selected" 
                    type="checkbox" 
                    class="form-check-input" 
                    :id="`selectItem${item.id}`"
                  >
                </div>
              </td>
              <td>
                <div class="product-info d-flex">
                  <router-link :to="`/product/${item.product_id}`" class="me-3">
                    <img :src="item.image_url" :alt="item.name" class="img-fluid" style="width: 80px; height: 80px; object-fit: cover;">
                  </router-link>
                  <div>
                    <h5 class="mb-1">
                      <router-link :to="`/product/${item.product_id}`" class="text-decoration-none text-dark">
                        {{ item.name }}
                      </router-link>
                    </h5>
                  </div>
                </div>
              </td>
              <td>¥{{ parseFloat(item.price || 0).toFixed(2) }}</td>
              <td>
                <div class="quantity-control d-flex align-items-center">
                  <button 
                    @click="decreaseQuantity(item)" 
                    class="btn btn-outline-secondary" 
                    type="button"
                    :disabled="item.quantity <= 1"
                  >-
                  </button>
                  <input 
                    v-model.number="item.quantity" 
                    type="number" 
                    class="form-control text-center" 
                    style="width: 60px;"
                    min="1"
                    @change="updateQuantity(item)"
                  >
                  <button 
                    @click="increaseQuantity(item)" 
                    class="btn btn-outline-secondary" 
                    type="button"
                  >+
                  </button>
                </div>
              </td>
              <td class="subtotal">¥{{ (item.price * item.quantity).toFixed(2) }}</td>
              <td>
                <button @click="confirmRemoveItem(item.id)" class="btn btn-outline-danger btn-sm">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 购物车底部 -->
      <div class="cart-footer mt-4 p-4 bg-light rounded">
        <div class="row">
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <button @click="confirmRemoveSelected" class="btn btn-outline-danger me-3">
                删除选中商品
              </button>
              <button @click="confirmClearCart" class="btn btn-outline-secondary">
                清空购物车
              </button>
            </div>
          </div>
          <div class="col-md-6">
            <div class="d-flex flex-column align-items-end">
              <div class="total-price mb-3">
                <span class="total-label">合计:</span>
                <span class="total-value">¥{{ totalPrice.toFixed(2) }}</span>
              </div>
              <button 
                @click="checkout" 
                class="btn btn-primary btn-lg"
                :disabled="selectedCount === 0"
              >
                结算 ({{ selectedCount }})
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐商品 -->
    <div v-if="cartStore.items.length > 0" class="recommended-products mt-10">
      <h3 class="mb-4">为您推荐</h3>
      <div class="row">
        <div v-for="product in recommendedProducts" :key="product.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
          <div class="product-card card h-100">
            <router-link :to="`/product/${product.id}`" class="text-decoration-none">
              <img :src="product.image_url" :alt="product.name" class="card-img-top">
              <div class="card-body">
                <h5 class="card-title text-truncate">{{ product.name }}</h5>
                <div class="price">¥{{ parseFloat(product.price || 0).toFixed(2) }}</div>
                <div class="sold-count">已售 {{ product.sold_count }}</div>
              </div>
            </router-link>
            <div class="card-footer">
              <button @click="addToCart(product)" class="btn btn-primary w-100">
                加入购物车
              </button>
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
import { useCartStore } from '../stores/cart'
import { useUserStore } from '../stores/user'

export default {
  name: 'Cart',
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    const userStore = useUserStore()
    const recommendedProducts = ref([])
    const loading = ref(false)

    const selectAll = computed({
      get: () => cartStore.items.length > 0 && cartStore.items.every(item => item.selected),
      set: (value) => cartStore.toggleSelectAll(value)
    })

    const handleSelectAll = () => {
      cartStore.toggleSelectAll(selectAll.value)
    }

    const fetchRecommendedProducts = async () => {
      try {
        loading.value = true
        // 模拟获取推荐商品
        recommendedProducts.value = [
          { id: 1, name: '苹果 iPhone 15 Pro Max 256GB', price: 9999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20smartphone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1234 },
          { id: 2, name: '华为 Mate 60 Pro 5G手机', price: 6999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20mobile%20phone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 856 },
          { id: 3, name: '索尼 WH-1000XM5 无线降噪耳机', price: 2499.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20headphones%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 2341 },
          { id: 4, name: 'MacBook Pro 14英寸 M3芯片', price: 12999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20laptop%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 567 }
        ]
      } catch (error) {
        console.error('Failed to fetch recommended products:', error)
        recommendedProducts.value = []
      } finally {
        loading.value = false
      }
    }

    const increaseQuantity = (item) => {
      if (item) {
        item.quantity = (item.quantity || 0) + 1
        cartStore.updateQuantity(item.id, item.quantity)
      }
    }

    const decreaseQuantity = (item) => {
      if (item && item.quantity > 1) {
        item.quantity--
        cartStore.updateQuantity(item.id, item.quantity)
      }
    }

    const updateQuantity = (item) => {
      if (item) {
        const newQuantity = Math.max(1, parseInt(item.quantity) || 1)
        item.quantity = newQuantity
        cartStore.updateQuantity(item.id, newQuantity)
      }
    }

    const confirmRemoveItem = async (itemId) => {
      console.log('准备删除单个商品，itemId:', itemId)
      if (!itemId) return
      
      const confirmed = window.confirm('确定要删除这件商品吗？')
      console.log('删除确认结果:', confirmed)
      if (confirmed) {
        console.log('执行删除单个商品')
        try {
          await cartStore.removeFromCart(itemId)
        } catch (error) {
          console.error('删除商品失败:', error)
          alert('删除商品失败，请重试')
        }
      }
    }

    const confirmRemoveSelected = async () => {
      console.log('准备删除选中商品')
      const selectedItems = cartStore.items.filter(item => item.selected)
      if (selectedItems.length === 0) {
        alert('请先选择要删除的商品！')
        return
      }
      // 先显示确认框
      const confirmed = window.confirm(`确定要删除选中的 ${selectedItems.length} 件商品吗？`)
      console.log('删除选中确认结果:', confirmed)
      // 只有在用户确认后才执行删除操作
      if (confirmed) {
        console.log('执行删除选中商品')
        try {
          await cartStore.removeSelected()
        } catch (error) {
          console.error('删除选中商品失败:', error)
          alert('删除选中商品失败，请重试')
        }
      }
    }

    const confirmClearCart = async () => {
      console.log('准备清空购物车')
      if (cartStore.items.length === 0) {
        alert('购物车已经是空的！')
        return
      }
      // 先显示确认框
      const confirmed = window.confirm('确定要清空购物车吗？此操作不可恢复！')
      console.log('清空确认结果:', confirmed)
      // 只有在用户确认后才执行清空操作
      if (confirmed) {
        console.log('执行清空购物车')
        try {
          await cartStore.clearCart()
        } catch (error) {
          console.error('清空购物车失败:', error)
          alert('清空购物车失败，请重试')
        }
      }
    }

    const addToCart = async (product) => {
      if (product) {
        try {
          await cartStore.addToCart(product, 1)
          alert('商品已添加到购物车！')
        } catch (error) {
          console.error('添加商品失败:', error)
          alert('添加商品失败，请重试')
        }
      }
    }

    const checkout = () => {
      const selectedItems = cartStore.items.filter(item => item.selected)
      if (selectedItems.length > 0) {
        router.push('/checkout')
      } else {
        alert('请先选择要结算的商品！')
      }
    }

    const totalPrice = computed(() => {
      return cartStore.items
        .filter(item => item.selected)
        .reduce((total, item) => total + (item.price || 0) * (item.quantity || 0), 0)
    })

    const selectedCount = computed(() => {
      return cartStore.items.filter(item => item.selected).length
    })

    onMounted(async () => {
      // 如果用户已登录，从后端获取购物车数据
      if (userStore.isLoggedIn) {
        await cartStore.fetchCartFromServer()
      } else {
        // 用户未登录，从localStorage加载购物车数据
        cartStore.loadFromLocalStorage()
      }
      fetchRecommendedProducts()
    })

    return {
      cartStore,
      recommendedProducts,
      loading,
      selectAll,
      totalPrice,
      selectedCount,
      handleSelectAll,
      increaseQuantity,
      decreaseQuantity,
      updateQuantity,
      confirmRemoveItem,
      confirmRemoveSelected,
      confirmClearCart,
      addToCart,
      checkout
    }
  }
}
</script>

<style scoped>
.empty-cart {
  min-height: 400px;
}

.empty-icon {
  font-size: 4rem;
  color: #6c757d;
}

.cart-items {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.subtotal {
  font-weight: bold;
  color: #dc3545;
}

.cart-footer {
  border-top: 1px solid #dee2e6;
}

.total-label {
  font-size: 1.1rem;
  margin-right: 10px;
}

.total-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #dc3545;
}

.recommended-products {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.product-card .card-img-top {
  height: 150px;
  object-fit: cover;
}

.price {
  color: #dc3545;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.sold-count {
  font-size: 0.8rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .cart-items {
    padding: 10px;
  }
  
  .product-info {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .product-info img {
    margin-bottom: 10px;
  }
  
  .cart-footer {
    flex-direction: column;
    align-items: stretch;
  }
  
  .cart-footer .col-md-6 {
    margin-bottom: 20px;
  }
  
  .cart-footer .d-flex {
    justify-content: center;
  }
}
</style>