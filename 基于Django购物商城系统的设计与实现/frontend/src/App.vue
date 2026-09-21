<template>
  <div class="app">
    <!-- 顶部导航栏 -->
    <header class="navbar navbar-expand-lg navbar-light bg-light sticky-top">
      <div class="container">
        <router-link to="/" class="navbar-brand text-primary fw-bold fs-3">
          电商商城
        </router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/" class="nav-link">首页</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                商品分类
              </a>
              <ul class="dropdown-menu">
                <li v-for="category in categories" :key="category.id">
                  <router-link :to="`/category/${category.id}`" class="dropdown-item">
                    {{ category.name }}
                  </router-link>
                </li>
              </ul>
            </li>
          </ul>
          
          <!-- 搜索框 -->
          <form class="d-flex me-3" @submit.prevent="search">
            <input 
              v-model="searchKeyword" 
              type="search" 
              class="form-control me-2" 
              placeholder="搜索商品"
            >
            <button type="submit" class="btn btn-primary search-btn">
              搜索
            </button>
          </form>
          
          <!-- 用户操作 -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/cart" class="nav-link position-relative">
                购物车
                <span v-if="cartCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                  {{ cartCount }}
                </span>
              </router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/login" class="nav-link">登录</router-link>
            </li>
            <li class="nav-item" v-else>
              <router-link to="/profile" class="nav-link">个人中心</router-link>
            </li>
          </ul>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="container py-4">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 页脚 -->
    <footer class="bg-light py-4 mt-4">
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <h5 class="text-primary">关于我们</h5>
            <p>电商商城是一个专业的在线购物平台，为您提供优质的商品和服务。</p>
          </div>
          <div class="col-md-4">
            <h5 class="text-primary">快速链接</h5>
            <ul class="list-unstyled">
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/profile">个人中心</router-link></li>
              <li><router-link to="/cart">购物车</router-link></li>
            </ul>
          </div>
          <div class="col-md-4">
            <h5 class="text-primary">联系我们</h5>
            <p>客服电话：400-123-4567</p>
            <p>邮箱：service@example.com</p>
          </div>
        </div>
        <div class="text-center mt-4 text-muted">
          <p>&copy; 2026 电商商城. 保留所有权利.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'
import { useCartStore } from './stores/cart'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const cartStore = useCartStore()
    
    const categories = ref([])
    const searchKeyword = ref('')
    
    const cartCount = computed(() => cartStore.totalCount)
    
    // 获取分类列表
    const fetchCategories = async () => {
      try {
        const response = await fetch('/api/products/categories/')
        if (response.ok) {
          categories.value = await response.json()
        }
      } catch (error) {
        console.error('获取分类失败:', error)
      }
    }
    
    // 搜索功能
    const search = () => {
      if (searchKeyword.value.trim()) {
        router.push({
          path: '/search',
          query: { keyword: searchKeyword.value.trim() }
        })
      }
    }
    
    onMounted(() => {
      fetchCategories()
    })
    
    return {
      categories,
      searchKeyword,
      search,
      isLoggedIn: userStore.isLoggedIn,
      cartCount
    }
  }
}
</script>

<style>
/* 全局样式 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  background-color: #f8f9fa;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 自定义样式 */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* 导航栏样式 */
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar .container {
  max-width: 800px;
}

/* 商品卡片样式 */
.product-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.product-card img {
  height: 200px;
  object-fit: cover;
}

/* 按钮样式 */
.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0069d9;
  border-color: #0062cc;
}

/* 搜索按钮样式 */
.search-btn {
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* 价格样式 */
.price {
  color: #dc3545;
  font-weight: bold;
  font-size: 1.2rem;
}

/* 加载动画 */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.spinner {
  width: 3rem;
  height: 3rem;
}
</style>
