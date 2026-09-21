<template>
  <div class="home">
    <!-- 轮播图 -->
    <div id="carouselExampleIndicators" class="carousel slide mb-6 position-relative" data-bs-ride="carousel">
      <!-- 分类导航（浮于轮播图上方 -->
      <div class="category-nav-top">
        <div class="category-row d-flex align-items-center flex-wrap">
          <div class="category-toggle" @click="toggleCategories">
            <span class="d-flex align-items-center">
              <i class="bi bi-list-ul me-2"></i>
              商品分类
              <i :class="['bi', categoriesCollapsed ? 'bi-chevron-down' : 'bi-chevron-up']" class="ms-2"></i>
            </span>
          </div>
          <div class="category-items d-flex flex-wrap">
            <router-link 
              v-for="category in parentCategories" 
              :key="category.id" 
              :to="`/category/${category.id}`" 
              class="category-tag"
            >
              {{ category.name }}
            </router-link>
          </div>
        </div>
        <div v-show="!categoriesCollapsed" class="category-content">
          <div class="row">
            <div v-for="(category, index) in displayCategories" :key="category.id" class="col-lg-2 col-md-3 col-sm-4 col-6 mb-3">
              <router-link :to="`/category/${category.id}`" class="category-item text-center">
                <div class="category-icon mb-2">
                  <i :class="['bi', getCategoryIcon(category.name)]"></i>
                </div>
                <div class="category-name">{{ category.name }}</div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=e-commerce%20website%20banner%20with%20promotional%20products%2C%20modern%20design%2C%20high%20quality&image_size=landscape_16_9" class="d-block w-100" alt="促销活动">
        </div>
        <div class="carousel-item">
          <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=e-commerce%20website%20banner%20with%20electronics%20products%2C%20modern%20design%2C%20high%20quality&image_size=landscape_16_9" class="d-block w-100" alt="电子产品">
        </div>
        <div class="carousel-item">
          <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=e-commerce%20website%20banner%20with%20fashion%20clothing%2C%20modern%20design%2C%20high%20quality&image_size=landscape_16_9" class="d-block w-100" alt="时尚服饰">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <!-- 热门商品 -->
    <div class="hot-products mb-6">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>🔥 热门商品</h3>
        <router-link to="/search?hot=true" class="text-primary">查看更多</router-link>
      </div>
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
        <p class="mt-3">正在加载商品...</p>
      </div>
      <div v-else-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      <div v-else class="row">
        <div v-for="product in products" :key="product.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
          <div class="product-card card h-100">
            <router-link :to="`/product/${product.id}`" class="text-decoration-none">
              <div class="product-image-container">
                <img :src="product.image_url" :alt="product.name" class="card-img-top" loading="lazy">
              </div>
              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <div class="price">¥{{ parseFloat(product.price || 0).toFixed(2) }}</div>
                <div class="sold-count">{{ product.sold_count }}</div>
              </div>
            </router-link>
            <div class="card-footer bg-transparent border-top-0">
              <button @click="addToCart(product)" class="btn btn-primary w-100">
                <i class="bi bi-cart-plus me-1"></i>
                加入购物车
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新品上市 -->
    <div class="new-products mb-6">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>🆕 新品上市</h3>
        <router-link to="/search?new=true" class="text-primary">查看更多</router-link>
      </div>
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
      </div>
      <div v-else-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      <div v-else class="row">
        <div v-for="(product, index) in products.slice().reverse()" :key="product.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
          <div class="product-card card h-100">
            <router-link :to="`/product/${product.id}`" class="text-decoration-none">
              <div class="product-image-container">
                <div class="badge-new">新品</div>
                <img :src="product.image_url" :alt="product.name" class="card-img-top" loading="lazy">
              </div>
              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <div class="price">¥{{ parseFloat(product.price || 0).toFixed(2) }}</div>
                <div class="sold-count">{{ product.sold_count }}</div>
              </div>
            </router-link>
            <div class="card-footer bg-transparent border-top-0">
              <button @click="addToCart(product)" class="btn btn-primary w-100">
                <i class="bi bi-cart-plus me-1"></i>
                加入购物车
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐商品 -->
    <div class="recommended-products">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>💝 为您推荐</h3>
        <router-link to="/search?recommended=true" class="text-primary">查看更多</router-link>
      </div>
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
      </div>
      <div v-else-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      <div v-else class="row">
        <div v-for="(product, index) in products" :key="product.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
          <div class="product-card card h-100">
            <router-link :to="`/product/${product.id}`" class="text-decoration-none">
              <div class="product-image-container">
                <img :src="product.image_url" :alt="product.name" class="card-img-top" loading="lazy">
              </div>
              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <div class="price">¥{{ parseFloat(product.price || 0).toFixed(2) }}</div>
                <div class="sold-count">{{ product.sold_count }}</div>
              </div>
            </router-link>
            <div class="card-footer bg-transparent border-top-0">
              <button @click="addToCart(product)" class="btn btn-primary w-100">
                <i class="bi bi-cart-plus me-1"></i>
                加入购物车
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 回到顶部按钮 -->
    <button 
      v-show="showBackToTop" 
      @click="scrollToTop" 
      class="back-to-top"
    >
      <i class="bi bi-arrow-up me-1"></i>
      <span>回到顶部</span>
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useCartStore } from '../stores/cart'

export default {
  name: 'Home',
  setup() {
    const cartStore = useCartStore()
    const categories = ref([])
    const products = ref([])
    const categoriesCollapsed = ref(true)
    const loading = ref(false)
    const error = ref(null)

    const toggleCategories = () => {
      console.log('点击切换分类，当前状态:', categoriesCollapsed.value)
      categoriesCollapsed.value = !categoriesCollapsed.value
      console.log('切换后状态:', categoriesCollapsed.value)
    }

    const parentCategories = computed(() => {
      const result = categories.value.filter(cat => !cat.parent)
      console.log('parentCategories:', result)
      return result
    })

    const displayCategories = computed(() => {
      return categories.value
    })

    const getCategoryIcon = (name) => {
      const iconMap = {
        '数码': 'bi-phone',
        '手机': 'bi-smartwatch',
        '电脑': 'bi-laptop',
        '平板': 'bi-tablet',
        '智能手表': 'bi-smartwatch',
        '耳机': 'bi-headphones',
        '家电': 'bi-tv',
        '电视': 'bi-tv',
        '空调': 'bi-fan',
        '冰箱': 'bi-house',
        '洗衣机': 'bi-stars',
        '厨房电器': 'bi-gear',
        '服饰': 'bi-person',
        '男装': 'bi-person',
        '女装': 'bi-person',
        '童装': 'bi-person',
        '鞋靴': 'bi-activity',
        '箱包': 'bi-bag',
        '美妆': 'bi-heart',
        '护肤': 'bi-heart',
        '彩妆': 'bi-palette',
        '香水': 'bi-droplet',
        '个护': 'bi-emoji-smile',
        '美发': 'bi-scissors',
        '食品': 'bi-egg',
        '零食': 'bi-cookie',
        '生鲜': 'bi-apple',
        '饮料': 'bi-cup-hot',
        '粮油': 'bi-basket',
        '酒水': 'bi-cup',
        '图书': 'bi-book',
        '小说': 'bi-book',
        '教育': 'bi-book',
        '科技': 'bi-lightbulb',
        '经管': 'bi-graph-up',
        '文学': 'bi-journal'
      }
      return iconMap[name] || 'bi-box'
    }

    const fetchCategories = async () => {
      try {
        const response = await fetch('/api/products/categories/')
        if (response.ok) {
          categories.value = await response.json()
        } else {
          throw new Error('API返回错误')
        }
      } catch (error) {
        console.error('获取分类失败，使用模拟数据:', error)
        categories.value = [
          { id: 1, name: '数码', parent: null },
          { id: 2, name: '手机', parent: 1 },
          { id: 3, name: '电脑', parent: 1 },
          { id: 4, name: '平板', parent: 1 },
          { id: 5, name: '智能手表', parent: 1 },
          { id: 6, name: '耳机', parent: 1 },
          { id: 7, name: '家电', parent: null },
          { id: 8, name: '电视', parent: 7 },
          { id: 9, name: '空调', parent: 7 },
          { id: 10, name: '冰箱', parent: 7 },
          { id: 11, name: '洗衣机', parent: 7 },
          { id: 12, name: '厨房电器', parent: 7 },
          { id: 13, name: '服饰', parent: null },
          { id: 14, name: '男装', parent: 13 },
          { id: 15, name: '女装', parent: 13 },
          { id: 16, name: '童装', parent: 13 },
          { id: 17, name: '鞋靴', parent: 13 },
          { id: 18, name: '箱包', parent: 13 },
          { id: 19, name: '美妆', parent: null },
          { id: 20, name: '护肤', parent: 19 },
          { id: 21, name: '彩妆', parent: 19 },
          { id: 22, name: '香水', parent: 19 },
          { id: 23, name: '个护', parent: 19 },
          { id: 24, name: '美发', parent: 19 },
          { id: 25, name: '食品', parent: null },
          { id: 26, name: '零食', parent: 25 },
          { id: 27, name: '生鲜', parent: 25 },
          { id: 28, name: '饮料', parent: 25 },
          { id: 29, name: '粮油', parent: 25 },
          { id: 30, name: '酒水', parent: 25 },
          { id: 31, name: '图书', parent: null },
          { id: 32, name: '小说', parent: 31 },
          { id: 33, name: '教育', parent: 31 },
          { id: 34, name: '科技', parent: 31 },
          { id: 35, name: '经管', parent: 31 },
          { id: 36, name: '文学', parent: 31 }
        ]
      }
    }

    const fetchProducts = async () => {
      loading.value = true
      error.value = null
      try {
        const response = await fetch('/api/products/products/')
        if (response.ok) {
          products.value = await response.json()
          products.value.forEach((product, index) => {
            product.image_url = `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(product.name)}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd`
            product.sold_count = Math.floor(Math.random() * 1000) + 50
            product.price = parseFloat(product.price)
          })
        } else {
          throw new Error('API返回错误')
        }
      } catch (err) {
        console.error('获取商品失败，使用模拟数据:', err)
        products.value = [
          { id: 1, name: '苹果 iPhone 15 Pro Max 256GB', price: 9999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20smartphone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1234 },
          { id: 2, name: '华为 Mate 60 Pro 5G手机', price: 6999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20mobile%20phone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 856 },
          { id: 3, name: '索尼 WH-1000XM5 无线降噪耳机', price: 2499.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20headphones%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 2341 },
          { id: 4, name: 'MacBook Pro 14英寸 M3芯片', price: 12999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20laptop%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 567 },
          { id: 5, name: '戴森 V15 Detect 无线吸尘器', price: 4990.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20vacuum%20cleaner%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 789 },
          { id: 6, name: '任天堂 Switch OLED 游戏机', price: 2199.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20game%20console%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1876 },
          { id: 7, name: 'SK-II 神仙水护肤精华 230ml', price: 1590.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20skincare%20cosmetics%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 3456 },
          { id: 8, name: 'iPad Pro 12.9英寸 M2芯片', price: 8999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20tablet%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 432 },
          { id: 9, name: '小米空气净化器 4 Pro', price: 1499.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20air%20purifier%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 987 },
          { id: 10, name: '佳能 EOS R6 Mark II 全画幅相机', price: 16999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20camera%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 234 },
          { id: 11, name: '优衣库 男士羽绒服 轻薄款', price: 399.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20jacket%20clothing%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 5678 },
          { id: 12, name: '三只松鼠 坚果大礼包 1kg', price: 99.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20nuts%20snacks%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 8901 },
          { id: 13, name: 'Kindle Paperwhite 电子书阅读器', price: 999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20ebook%20reader%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1234 },
          { id: 14, name: 'Beats Studio Buds+ 真无线耳机', price: 1099.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20earbuds%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 2345 },
          { id: 15, name: '兰蔻小黑瓶精华肌底液 100ml', price: 1080.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20serum%20cosmetics%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 4567 },
          { id: 16, name: '乐高 哈利波特 霍格沃茨城堡', price: 3999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20lego%20toy%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 678 }
        ]
      } finally {
        loading.value = false
      }
    }

    const addToCart = (product) => {
      cartStore.addToCart(product, 1)
    }

    const showBackToTop = ref(false)
    
    const handleScroll = () => {
      showBackToTop.value = window.scrollY > 300
    }
    
    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }

    onMounted(() => {
      fetchCategories()
      fetchProducts()
      window.addEventListener('scroll', handleScroll)
    })
    
    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
    })

    return {
      categories,
      products,
      categoriesCollapsed,
      loading,
      error,
      parentCategories,
      displayCategories,
      toggleCategories,
      getCategoryIcon,
      addToCart,
      showBackToTop,
      scrollToTop
    }
  }
}
</script>

<style scoped>
.category-nav-top {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  background: rgba(255, 255, 255, 0.98);
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.category-row {
  gap: 10px;
  align-items: center;
}

.category-toggle {
  cursor: pointer;
  color: #333;
  user-select: none;
  font-size: 1rem;
  font-weight: 600;
  flex-shrink: 0;
  padding: 6px 0;
}

.category-toggle span {
  display: flex;
  align-items: center;
}

.category-items {
  gap: 6px;
  flex: 1;
  align-items: center;
}

.category-tag {
  padding: 4px 10px;
  border-radius: 16px;
  color: #333;
  text-decoration: none;
  font-size: 0.85rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.category-tag:hover {
  background: #f5f5f5;
  color: #ff4400;
}

.category-content {
  margin-top: 10px;
  transition: all 0.3s ease;
}

.category-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 12px 8px;
  border-radius: 6px;
  background: white;
  transition: all 0.2s ease;
  border: 1px solid #f5f5f5;
  text-decoration: none;
  height: 100%;
}

.category-item:hover {
  background: #fafafa;
  border-color: #ddd;
  transform: translateY(-1px);
}

.category-icon {
  font-size: 1.8rem;
  color: #666;
}

.category-name {
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
}

.carousel-item img {
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
  padding-top: 50px;
}

/* 商品区域标题简约样式 */
.hot-products h3,
.new-products h3,
.recommended-products h3 {
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
}

.hot-products .text-primary,
.new-products .text-primary,
.recommended-products .text-primary {
  color: #666 !important;
  font-size: 0.9rem;
  text-decoration: none;
}

.hot-products .text-primary:hover,
.new-products .text-primary:hover,
.recommended-products .text-primary:hover {
  color: #333 !important;
}

/* 淘宝风格商品卡片 */
.product-card {
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  background: #fff;
  transition: all 0.2s ease;
  position: relative;
}

.product-card:hover {
  border-color: #ddd;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.product-image-container {
  position: relative;
  overflow: hidden;
  padding: 5px;
  background: #fff;
}

.product-card .card-img-top {
  height: 220px;
  width: 100%;
  object-fit: cover;
  border-radius: 2px;
  transition: opacity 0.2s ease;
}

.product-card:hover .card-img-top {
  opacity: 0.95;
}

.product-card .card-body {
  padding: 10px;
}

.product-card .card-title {
  font-size: 12px;
  line-height: 18px;
  height: 36px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #333;
  margin-bottom: 8px;
  font-weight: 400;
}

.product-card .card-text {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
  display: none;
}

.badge-new {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #ff4400;
  color: white;
  padding: 2px 8px;
  border-radius: 2px;
  font-size: 11px;
  font-weight: 500;
  z-index: 10;
}

.price {
  color: #ff4400;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 4px;
  line-height: 1;
}

.price::before {
  content: '¥';
  font-size: 14px;
  font-weight: 400;
  margin-right: 2px;
}

.sold-count {
  font-size: 12px;
  color: #999;
  line-height: 1;
}

.sold-count::after {
  content: '人付款';
}

.product-card .card-footer {
  padding: 0 10px 10px 10px;
  border-top: none;
  background: transparent;
}

.product-card .btn-primary {
  background: #ff4400;
  border-color: #ff4400;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 2px;
  transition: all 0.2s ease;
}

.product-card .btn-primary:hover {
  background: #f22d00;
  border-color: #f22d00;
}

/* 回到顶部按钮 */
.back-to-top {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: auto;
  height: 44px;
  padding: 0 16px;
  border-radius: 22px;
  background: #fff;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #666;
  transition: all 0.3s ease;
  z-index: 1000;
  white-space: nowrap;
}

.back-to-top:hover {
  background: #f5f5f5;
  border-color: #ccc;
  color: #333;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .carousel-item img {
    height: 250px;
    padding-top: 50px;
  }
  
  .product-card .card-img-top {
    height: 160px;
  }
  
  .category-icon {
    font-size: 1.6rem;
  }
  
  .back-to-top {
    bottom: 20px;
    right: 20px;
    height: 40px;
    padding: 0 12px;
    font-size: 13px;
  }
}
</style>
