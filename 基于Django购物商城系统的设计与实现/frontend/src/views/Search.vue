<template>
  <div class="search">
    <!-- 搜索框 -->
    <div class="search-box mb-6 p-4 bg-light rounded">
      <form @submit.prevent="performSearch" class="d-flex">
        <input 
          v-model="searchKeyword" 
          type="search" 
          class="form-control me-2" 
          placeholder="搜索商品"
          required
        >
        <button type="submit" class="btn btn-primary">
          搜索
        </button>
      </form>
    </div>

    <!-- 搜索结果标题 -->
    <h2 class="mb-4">
      搜索结果: {{ searchKeyword }}
      <span v-if="totalResults > 0" class="text-muted fs-5">
        (共 {{ totalResults }} 件商品)
      </span>
    </h2>

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

    <!-- 搜索结果 -->
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
        <i class="bi bi-search"></i>
      </div>
      <h4 class="mb-2">未找到商品</h4>
      <p class="text-muted">没有找到与 "{{ searchKeyword }}" 相关的商品</p>
      <p class="text-muted mb-4">请尝试其他关键词或浏览分类</p>
      <div class="d-flex justify-content-center gap-2">
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
        <button @click="clearSearch" class="btn btn-outline-primary">清空搜索</button>
      </div>
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
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'

export default {
  name: 'Search',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const cartStore = useCartStore()
    const searchKeyword = ref('')
    const products = ref([])
    const loading = ref(false)
    const priceRange = ref({ min: null, max: null })
    const sortBy = ref('default')
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalResults = ref(0)

    // 计算总页数
    const totalPages = computed(() => {
      return Math.ceil(totalResults.value / pageSize.value)
    })

    // 执行搜索
    const performSearch = async () => {
      if (searchKeyword.value.trim()) {
        currentPage.value = 1
        fetchSearchResults()
        // 更新URL参数
        router.push({
          path: '/search',
          query: { keyword: searchKeyword.value.trim() }
        })
      }
    }

    // 获取搜索结果
    const fetchSearchResults = async () => {
      loading.value = true
      try {
        // 构建查询参数
        let queryParams = new URLSearchParams()
        queryParams.append('keyword', searchKeyword.value.trim())
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

        // 获取搜索结果
        const response = await fetch(`/api/products/search/?${queryParams.toString()}`)
        if (response.ok) {
          const data = await response.json()
          products.value = data.results
          totalResults.value = data.count
        }
      } catch (error) {
        console.error('搜索商品失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 筛选商品
    const filterProducts = () => {
      currentPage.value = 1
      fetchSearchResults()
    }

    // 切换分页
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchSearchResults()
      }
    }

    // 添加到购物车
    const addToCart = (product) => {
      cartStore.addToCart(product, 1)
    }

    // 清空搜索
    const clearSearch = () => {
      searchKeyword.value = ''
      priceRange.value = { min: null, max: null }
      sortBy.value = 'default'
      currentPage.value = 1
      products.value = []
      totalResults.value = 0
    }

    // 监听路由参数变化
    watch(() => route.query.keyword, (newKeyword) => {
      if (newKeyword) {
        searchKeyword.value = newKeyword
        currentPage.value = 1
        fetchSearchResults()
      }
    })

    // 监听排序变化
    watch(sortBy, () => {
      currentPage.value = 1
      fetchSearchResults()
    })

    onMounted(() => {
      // 从URL获取搜索关键词
      if (route.query.keyword) {
        searchKeyword.value = route.query.keyword
        fetchSearchResults()
      }
    })

    return {
      searchKeyword,
      products,
      loading,
      priceRange,
      sortBy,
      currentPage,
      totalPages,
      totalResults,
      performSearch,
      filterProducts,
      changePage,
      addToCart,
      clearSearch
    }
  }
}
</script>

<style scoped>
/* 搜索框样式 */
.search-box {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-box input {
  font-size: 1.1rem;
  padding: 10px 15px;
}

/* 商品卡片样式 */
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
  height: 200px;
  object-fit: cover;
}

.price {
  color: #dc3545;
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 5px;
}

.sold-count {
  font-size: 0.8rem;
  color: #6c757d;
}

/* 空状态样式 */
.empty-state {
  background-color: #f8f9fa;
  border-radius: 8px;
  min-height: 300px;
}

.empty-icon {
  font-size: 4rem;
  color: #6c757d;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .product-card .card-img-top {
    height: 150px;
  }
}
</style>