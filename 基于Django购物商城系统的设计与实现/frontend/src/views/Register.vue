<template>
  <div class="register">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="register-card p-6 bg-white rounded shadow">
            <h2 class="text-center mb-6">用户注册</h2>
            
            <!-- 注册表单 -->
            <form @submit.prevent="register" class="needs-validation" novalidate>
              <!-- 用户名 -->
              <div class="mb-4">
                <label for="username" class="form-label">用户名</label>
                <input 
                  v-model="registerForm.username" 
                  type="text" 
                  class="form-control" 
                  id="username"
                  required
                  placeholder="请输入用户名"
                >
                <div class="invalid-feedback">
                  请输入用户名
                </div>
              </div>
              
              <!-- 邮箱 -->
              <div class="mb-4">
                <label for="email" class="form-label">邮箱</label>
                <input 
                  v-model="registerForm.email" 
                  type="email" 
                  class="form-control" 
                  id="email"
                  required
                  placeholder="请输入邮箱"
                >
                <div class="invalid-feedback">
                  请输入有效的邮箱地址
                </div>
              </div>
              
              <!-- 密码 -->
              <div class="mb-4">
                <label for="password" class="form-label">密码</label>
                <input 
                  v-model="registerForm.password" 
                  type="password" 
                  class="form-control" 
                  id="password"
                  required
                  placeholder="请输入密码（至少6位）"
                  minlength="6"
                >
                <div class="invalid-feedback">
                  密码长度至少为6位
                </div>
              </div>
              
              <!-- 确认密码 -->
              <div class="mb-4">
                <label for="confirmPassword" class="form-label">确认密码</label>
                <input 
                  v-model="registerForm.confirmPassword" 
                  type="password" 
                  class="form-control" 
                  id="confirmPassword"
                  required
                  placeholder="请再次输入密码"
                >
                <div class="invalid-feedback">
                  两次输入的密码不一致
                </div>
              </div>
              
              <!-- 验证码 -->
              <div class="mb-4">
                <label for="captcha" class="form-label">验证码</label>
                <div class="d-flex">
                  <input 
                    v-model="registerForm.captcha" 
                    type="text" 
                    class="form-control me-2" 
                    id="captcha"
                    required
                    placeholder="请输入验证码"
                  >
                  <button type="button" class="btn btn-outline-secondary" @click="getCaptcha">
                    {{ captchaText }}
                  </button>
                </div>
                <div class="invalid-feedback">
                  请输入验证码
                </div>
              </div>
              
              <!-- 同意协议 -->
              <div class="mb-6 form-check">
                <input 
                  v-model="registerForm.agreeTerms" 
                  type="checkbox" 
                  class="form-check-input" 
                  id="agreeTerms"
                  required
                >
                <label class="form-check-label" for="agreeTerms">
                  我已阅读并同意 <a href="#" class="text-primary">用户协议</a> 和 <a href="#" class="text-primary">隐私政策</a>
                </label>
                <div class="invalid-feedback">
                  请阅读并同意用户协议和隐私政策
                </div>
              </div>
              
              <!-- 注册按钮 -->
              <button 
                type="submit" 
                class="btn btn-primary w-100 py-2" 
                :disabled="loading"
              >
                <span v-if="loading">注册中...</span>
                <span v-else>注册</span>
              </button>
              
              <!-- 错误信息 -->
              <div v-if="error" class="mt-4 alert alert-danger">
                {{ error }}
              </div>
              
              <!-- 成功信息 -->
              <div v-if="success" class="mt-4 alert alert-success">
                {{ success }}
              </div>
            </form>
            
            <!-- 登录链接 -->
            <div class="mt-6 text-center">
              <p>已有账号？ <router-link to="/login" class="text-primary">立即登录</router-link></p>
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
  name: 'Register',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const registerForm = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      captcha: '',
      agreeTerms: false
    })
    const loading = ref(false)
    const error = ref('')
    const success = ref('')
    const captchaText = ref('获取验证码')
    const captchaCountdown = ref(0)

    // 获取验证码
    const getCaptcha = () => {
      if (captchaCountdown.value > 0) return
      
      // 验证邮箱格式
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(registerForm.value.email)) {
        error.value = '请输入有效的邮箱地址'
        return
      }

      // 开始倒计时
      captchaCountdown.value = 60
      captchaText.value = `${captchaCountdown.value}s后重新获取`
      
      const countdownInterval = setInterval(() => {
        captchaCountdown.value--
        captchaText.value = `${captchaCountdown.value}s后重新获取`
        
        if (captchaCountdown.value <= 0) {
          clearInterval(countdownInterval)
          captchaText.value = '获取验证码'
        }
      }, 1000)

      // 调用获取验证码API
      fetch('/api/accounts/send-captcha/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: registerForm.value.email })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          success.value = '验证码已发送到您的邮箱'
          error.value = ''
        } else {
          error.value = data.message || '发送验证码失败'
          success.value = ''
        }
      })
      .catch(err => {
        console.error('发送验证码错误:', err)
        error.value = '网络错误，请稍后重试'
        success.value = ''
      })
    }

    // 注册
    const register = async () => {
      // 验证表单
      const form = document.querySelector('form')
      if (!form.checkValidity()) {
        form.classList.add('was-validated')
        return
      }

      // 验证密码是否一致
      if (registerForm.value.password !== registerForm.value.confirmPassword) {
        error.value = '两次输入的密码不一致'
        return
      }

      loading.value = true
      error.value = ''
      success.value = ''

      try {
        // 调用注册API
        const response = await fetch('/api/accounts/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: registerForm.value.username,
            email: registerForm.value.email,
            password: registerForm.value.password,
            captcha: registerForm.value.captcha
          })
        })

        if (response.ok) {
          const data = await response.json()
          success.value = '注册成功，请登录'
          // 跳转到登录页面
          setTimeout(() => {
            router.push('/login')
          }, 2000)
        } else {
          const errorData = await response.json()
          error.value = errorData.message || '注册失败，请稍后重试'
        }
      } catch (err) {
        console.error('注册错误:', err)
        error.value = '网络错误，请稍后重试'
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
      registerForm,
      loading,
      error,
      success,
      captchaText,
      getCaptcha,
      register
    }
  }
}
</script>

<style scoped>
/* 注册卡片样式 */
.register-card {
  margin-top: 30px;
  margin-bottom: 30px;
  padding: 3rem;
  border-radius: 20px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .register-card {
    margin-top: 20px;
    margin-bottom: 20px;
    padding: 30px 20px;
    border-radius: 16px;
  }
}
</style>