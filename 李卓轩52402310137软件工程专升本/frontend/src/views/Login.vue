<template>
  <div class="login">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="login-card p-6 bg-white rounded shadow">
            <h2 class="text-center mb-6">用户登录</h2>
            
            <!-- 登录表单 -->
            <form @submit.prevent="login" class="needs-validation" novalidate>
              <!-- 用户名/邮箱 -->
              <div class="mb-4">
                <label for="username" class="form-label">用户名/邮箱</label>
                <input 
                  v-model="loginForm.username" 
                  type="text" 
                  class="form-control" 
                  id="username"
                  required
                  placeholder="请输入用户名或邮箱"
                >
                <div class="invalid-feedback">
                  请输入用户名或邮箱
                </div>
              </div>
              
              <!-- 密码 -->
              <div class="mb-4">
                <label for="password" class="form-label">密码</label>
                <input 
                  v-model="loginForm.password" 
                  type="password" 
                  class="form-control" 
                  id="password"
                  required
                  placeholder="请输入密码"
                >
                <div class="invalid-feedback">
                  请输入密码
                </div>
              </div>
              
              <!-- 记住我和忘记密码 -->
              <div class="d-flex justify-content-between align-items-center mb-6">
                <div class="form-check">
                  <input 
                    v-model="loginForm.remember" 
                    type="checkbox" 
                    class="form-check-input" 
                    id="remember"
                  >
                  <label class="form-check-label" for="remember">
                    记住我
                  </label>
                </div>
                <router-link to="/forgot-password" class="text-primary">
                  忘记密码？
                </router-link>
              </div>
              
              <!-- 登录按钮 -->
              <button 
                type="submit" 
                class="btn btn-primary w-100 py-2" 
                :disabled="loading"
              >
                <span v-if="loading">登录中...</span>
                <span v-else>登录</span>
              </button>
              
              <!-- 错误信息 -->
              <div v-if="error" class="mt-4 alert alert-danger">
                {{ error }}
              </div>
            </form>
            
            <!-- 注册链接 -->
            <div class="mt-6 text-center">
              <p>还没有账号？ <router-link to="/register" class="text-primary">立即注册</router-link></p>
            </div>
            
            <!-- 第三方登录 -->
            <div class="mt-6">
              <div class="divider text-center mb-4">
                <span class="text-muted">其他登录方式</span>
              </div>
              <div class="social-login d-flex justify-content-center gap-4">
                <button class="social-btn btn btn-outline-primary">
                  <i class="bi bi-wechat me-2"></i>微信登录
                </button>
                <button class="social-btn btn btn-outline-danger">
                  <i class="bi bi-qq me-2"></i>QQ登录
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const loginForm = ref({
      username: '',
      password: '',
      remember: false
    })
    const loading = ref(false)
    const error = ref('')

    // 登录
    const login = async () => {
      // 验证表单
      const form = document.querySelector('form')
      if (!form.checkValidity()) {
        form.classList.add('was-validated')
        return
      }

      loading.value = true
      error.value = ''

      try {
        // 调用store的登录方法
        const success = await userStore.login(
          loginForm.value.username,
          loginForm.value.password
        )
        if (success) {
          router.push('/')
        }
      } catch (err) {
        console.error('登录错误:', err)
        error.value = err.message || '网络错误，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      // 如果用户已登录，跳转到首页
      if (userStore.isLoggedIn) {
        router.push('/')
      }
    })

    return {
      loginForm,
      loading,
      error,
      login
    }
  }
}
</script>

<style scoped>
/* 登录卡片样式 */
.login-card {
  margin-top: 50px;
  margin-bottom: 50px;
  padding: 3rem;
  border-radius: 20px;
}

/* 分隔线样式 */
.divider {
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #dee2e6;
  z-index: 1;
}

.divider span {
  position: relative;
  background-color: #fff;
  padding: 0 20px;
  z-index: 2;
}

/* 社交登录按钮样式 */
.social-btn {
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .login-card {
    margin-top: 20px;
    margin-bottom: 20px;
    padding: 30px 20px;
  }
}
</style>