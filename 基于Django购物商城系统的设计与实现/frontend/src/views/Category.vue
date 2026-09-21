<template>
  <div class="category">
    <!-- 面包屑导航 -->
    <nav aria-label="breadcrumb" class="mb-4">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <router-link to="/">首页</router-link>
        </li>
        <li class="breadcrumb-item active" aria-current="page">
          {{ categoryName }}
        </li>
      </ol>
    </nav>

    <!-- 分类标题 -->
    <h2 class="mb-4">{{ categoryName }}</h2>

    <!-- 筛选和排序 -->
    <div class="filter-sort mb-4 p-3 bg-light rounded">
      <div class="row">
        <!-- 价格筛选 -->
        <div class="col-md-4 mb-3">
          <div class="d-flex align-items-center">
            <span class="me-3">价格:</span>
            <input v-model.number="priceRange.min" type="number" placeholder="最小" class="form-control me-2" style="width: 100px;">
            <span class="me-2">-</span>
            <input v-model.number="priceRange.max" type="number" placeholder="最大" class="form-control me-2" style="width: 100px;">
            <button @click="filterProducts" class="btn btn-sm btn-primary">筛选</button>
          </div>
        </div>

        <!-- 排序方式 -->
        <div class="col-md-4 mb-3">
          <div class="d-flex align-items-center">
            <span class="me-3">排序:</span>
            <select v-model="sortBy" class="form-select" style="width: 150px;">
              <option value="default">默认</option>
              <option value="price_asc">价格从低到高</option>
              <option value="price_desc">价格从高到低</option>
              <option value="sales">销量从高到低</option>
              <option value="newest">最新上架</option>
            </select>
          </div>
        </div>

        <!-- 商品数量 -->
        <div class="col-md-4 text-right">
          <span>共 {{ products.length }} 件商品</span>
        </div>
      </div>
    </div>

    <!-- 商品列表 -->
    <div v-if="products.length > 0" class="row">
      <div v-for="product in products" :key="product.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
        <div class="product-card card h-100">
          <router-link :to="`/product/${product.id}`" class="text-decoration-none">
            <img :src="product.image_url" :alt="product.name" class="card-img-top">
            <div class="card-body">
              <h5 class="card-title text-truncate">{{ product.name }}</h5>
              <p class="card-text text-truncate">{{ product.description }}</p>
              <div class="price">¥{{ product.price.toFixed(2) }}</div>
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

    <!-- 空状态 -->
    <div v-else class="empty-state text-center py-10">
      <div class="empty-icon mb-3">
        <i class="bi bi-box-seam"></i>
      </div>
      <h4 class="mb-2">暂无商品</h4>
      <p class="text-muted">该分类下暂无商品，请尝试其他分类</p>
      <router-link to="/" class="btn btn-primary mt-3">返回首页</router-link>
    </div>

    <!-- 分页 -->
    <div v-if="products.length > 0" class="pagination-container mt-6">
      <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button @click="changePage(currentPage - 1)" class="page-link">上一页</button>
          </li>
          <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
            <button @click="changePage(page)" class="page-link">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button @click="changePage(currentPage + 1)" class="page-link">下一页</button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '../stores/cart'

export default {
  name: 'Category',
  setup() {
    const route = useRoute()
    const cartStore = useCartStore()
    const categoryId = ref(route.params.id)
    const categoryName = ref('')
    const products = ref([])
    const loading = ref(false)
    const priceRange = ref({ min: null, max: null })
    const sortBy = ref('default')
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalItems = ref(0)

    // 计算总页数
    const totalPages = computed(() => {
      return Math.ceil(totalItems.value / pageSize.value)
    })

    // 获取分类名称和商品
    const fetchCategoryProducts = async () => {
      loading.value = true
      try {
        // 获取分类信息
        const categoryResponse = await fetch(`/api/products/categories/${categoryId.value}/`)
        if (categoryResponse.ok) {
          const categoryData = await categoryResponse.json()
          categoryName.value = categoryData.name
        }

        // 构建查询参数
        let queryParams = new URLSearchParams()
        queryParams.append('category_id', categoryId.value)
        queryParams.append('page', currentPage.value)
        queryParams.append('page_size', pageSize.value)

        // 添加价格筛选
        if (priceRange.value.min !== null && priceRange.value.min !== '') {
          queryParams.append('min_price', priceRange.value.min)
        }
        if (priceRange.value.max !== null && priceRange.value.max !== '') {
          queryParams.append('max_price', priceRange.value.max)
        }

        // 添加排序
        queryParams.append('sort_by', sortBy.value)

        // 获取商品列表
        const productsResponse = await fetch(`/api/products/?${queryParams.toString()}`)
        if (productsResponse.ok) {
          const data = await productsResponse.json()
          products.value = data.results
          totalItems.value = data.count
        }
      } catch (error) {
        console.error('获取分类商品失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 添加到购物车
    const addToCart = (product) => {
      cartStore.addToCart(product, 1)
    }

    // 筛选商品
    const filterProducts = () => {
      currentPage.value = 1
      fetchCategoryProducts()
    }

    // 切换分页
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchCategoryProducts()
      }
    }

    // 监听路由参数变化
    watch(() => route.params.id, (newId) => {
      categoryId.value = newId
      currentPage.value = 1
      fetchCategoryProducts()
    })

    // 监听排序变化
    watch(sortBy, () => {
      currentPage.value = 1
      fetchCategoryProducts()
    })

    onMounted(() => {
      fetchCategoryProducts()
    })

    return {
      categoryId,
      categoryName,
      products,
      loading,
      priceRange,
      sortBy,
      currentPage,
      totalPages,
      addToCart,
      filterProducts,
      changePage
    }
  }
}
</script>

<style scoped>
/* 淘宝风格商品卡片 */
.product-card {
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
  background: #fff;
  transition: all 0.2s ease;
  position: relative;
}

.product-card:hover {
  border-color: #ff4400;
  box-shadow: 0 0 10px rgba(255, 68, 0, 0.2);
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

/* 空状态样式 */
.empty-state {
  background-color: #f8f9fa;
  border-radius: 8px;
  min-height: 300px;
}

.empty-icon {
  font-size: 3rem;
  color: #6c757d;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .product-card .card-img-top {
    height: 150px;
  }
}
</style>