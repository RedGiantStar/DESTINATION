import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    addresses: []
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    currentUser: (state) => state.user
  },
  
  actions: {
    // 登录
    async login(username, password) {
      try {
        const response = await fetch('/api/accounts/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        })
        
        if (response.ok) {
          const data = await response.json()
          this.token = data.access
          this.user = data.user
          
          // 保存到本地存储
          localStorage.setItem('token', data.access)
          localStorage.setItem('user', JSON.stringify(data.user))
          
          return true
        } else {
          const error = await response.json()
          throw new Error(error.error || '登录失败')
        }
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },
    
    // 注册
    async register(userData) {
      try {
        const response = await fetch('/api/accounts/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
        })
        
        if (response.ok) {
          const data = await response.json()
          this.token = data.access
          this.user = data.user
          
          // 保存到本地存储
          localStorage.setItem('token', data.access)
          localStorage.setItem('user', JSON.stringify(data.user))
          
          return true
        } else {
          const error = await response.json()
          throw new Error(Object.values(error)[0][0] || '注册失败')
        }
      } catch (error) {
        console.error('注册失败:', error)
        throw error
      }
    },
    
    // 退出登录
    logout() {
      this.token = null
      this.user = null
      this.addresses = []
      
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
    
    // 获取用户信息
    async getUserProfile() {
      if (!this.token) return
      
      try {
        const response = await fetch('/api/accounts/profile/', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          this.user = data
          localStorage.setItem('user', JSON.stringify(data))
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    },
    
    // 获取用户地址
    async getAddresses() {
      if (!this.token) return
      
      try {
        const response = await fetch('/api/accounts/addresses/', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        })
        
        if (response.ok) {
          this.addresses = await response.json()
        }
      } catch (error) {
        console.error('获取地址失败:', error)
      }
    },
    
    // 添加地址
    async addAddress(addressData) {
      if (!this.token) return
      
      try {
        const response = await fetch('/api/accounts/addresses/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
          },
          body: JSON.stringify(addressData)
        })
        
        if (response.ok) {
          const newAddress = await response.json()
          this.addresses.push(newAddress)
          return newAddress
        }
      } catch (error) {
        console.error('添加地址失败:', error)
        throw error
      }
    }
  }
})
