import { defineStore } from 'pinia'
import { useUserStore } from './user'

export const useCartStore = defineStore('cart', {
  state: () => {
    try {
      const savedCart = localStorage.getItem('cart')
      return {
        items: savedCart ? JSON.parse(savedCart) : [],
        loading: false
      }
    } catch (error) {
      console.error('Failed to parse cart from localStorage:', error)
      return {
        items: [],
        loading: false
      }
    }
  },
  
  getters: {
    totalCount: (state) => state.items.reduce((total, item) => total + (item.quantity || 0), 0),
    totalAmount: (state) => state.items.reduce((total, item) => total + (item.price || 0) * (item.quantity || 0), 0),
    selectedItems: (state) => state.items.filter(item => item.selected),
    selectedTotalAmount: (state) => state.items.filter(item => item.selected).reduce((total, item) => total + (item.price || 0) * (item.quantity || 0), 0)
  },
  
  actions: {
    async addToCart(product, quantity = 1) {
      try {
        if (!product || !product.id) {
          console.error('Invalid product:', product)
          throw new Error('无效的商品信息')
        }
        
        const userStore = useUserStore()
        console.log('用户状态:', { isLoggedIn: userStore.isLoggedIn, token: userStore.token ? '存在' : '不存在' })
        
        if (userStore.isLoggedIn) {
          // 用户已登录，调用后端API
          try {
            const response = await fetch('/api/cart/items/add/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.token}`
              },
              body: JSON.stringify({
                product_id: product.id,
                quantity: quantity
              })
            })
            
            console.log('API响应状态:', response.status)
            
            if (response.ok) {
              // 添加成功后重新获取购物车数据
              await this.fetchCartFromServer()
            } else if (response.status === 401 || response.status === 403) {
              // Token无效或过期，清除本地存储并提示用户重新登录
              userStore.logout()
              throw new Error('登录已过期，请重新登录')
            } else {
              let error = '添加商品失败'
              try {
                const errorData = await response.json()
                console.log('API错误响应:', errorData)
                error = errorData.error || errorData.detail || error
              } catch (jsonError) {
                console.error('解析错误响应失败:', jsonError)
              }
              console.error('添加商品失败:', error)
              throw new Error(error)
            }
          } catch (apiError) {
            console.error('API调用失败:', apiError)
            throw apiError
          }
        } else {
          // 用户未登录，使用本地存储
          const existingItem = this.items.find(item => item.id === product.id)
          
          if (existingItem) {
            existingItem.quantity = (existingItem.quantity || 0) + quantity
          } else {
            this.items.push({
              id: product.id,
              product_id: product.id,
              name: product.name || 'Unknown Product',
              price: parseFloat(product.price || 0),
              quantity: quantity,
              image_url: product.image_url || '',
              selected: true
            })
          }
          
          this.saveToLocalStorage()
        }
      } catch (error) {
        console.error('添加商品到购物车失败:', error)
        throw error
      }
    },
    
    async updateQuantity(productId, quantity) {
      try {
        const userStore = useUserStore()
        
        if (userStore.isLoggedIn) {
          // 用户已登录，调用后端API
          try {
            const response = await fetch(`/api/cart/items/${productId}/update/`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.token}`
              },
              body: JSON.stringify({
                quantity: quantity
              })
            })
            
            if (response.ok) {
              // 更新成功后重新获取购物车数据
              await this.fetchCartFromServer()
            } else if (response.status === 401 || response.status === 403) {
              // Token无效或过期，清除本地存储并提示用户重新登录
              userStore.logout()
              throw new Error('登录已过期，请重新登录')
            } else {
              let error = '更新数量失败'
              try {
                const errorData = await response.json()
                error = errorData.error || error
              } catch (jsonError) {
                console.error('解析错误响应失败:', jsonError)
              }
              console.error('更新数量失败:', error)
              throw new Error(error)
            }
          } catch (apiError) {
            console.error('API调用失败:', apiError)
            throw apiError
          }
        } else {
          // 用户未登录，使用本地存储
          const item = this.items.find(item => item.id === productId)
          if (item) {
            item.quantity = Math.max(1, quantity || 1)
            this.saveToLocalStorage()
          }
        }
      } catch (error) {
        console.error('更新商品数量失败:', error)
        throw error
      }
    },
    
    async removeFromCart(productId) {
      try {
        const userStore = useUserStore()
        
        if (userStore.isLoggedIn) {
          // 用户已登录，调用后端API
          try {
            const response = await fetch(`/api/cart/items/${productId}/delete/`, {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${userStore.token}`
              }
            })
            
            if (response.ok) {
              // 删除成功后重新获取购物车数据
              await this.fetchCartFromServer()
            } else if (response.status === 401 || response.status === 403) {
              // Token无效或过期，清除本地存储并提示用户重新登录
              userStore.logout()
              throw new Error('登录已过期，请重新登录')
            } else {
              let error = '删除商品失败'
              try {
                const errorData = await response.json()
                error = errorData.error || error
              } catch (jsonError) {
                console.error('解析错误响应失败:', jsonError)
              }
              console.error('删除商品失败:', error)
              throw new Error(error)
            }
          } catch (apiError) {
            console.error('API调用失败:', apiError)
            throw apiError
          }
        } else {
          // 用户未登录，使用本地存储
          this.items = this.items.filter(item => item.id !== productId)
          this.saveToLocalStorage()
        }
      } catch (error) {
        console.error('删除商品失败:', error)
        throw error
      }
    },
    
    async removeSelected() {
      const userStore = useUserStore()
      
      if (userStore.isLoggedIn) {
        // 用户已登录，逐个删除选中商品
        const selectedItems = this.items.filter(item => item.selected)
        for (const item of selectedItems) {
          await this.removeFromCart(item.id)
        }
      } else {
        // 用户未登录，使用本地存储
        this.items = this.items.filter(item => !item.selected)
        this.saveToLocalStorage()
      }
    },
    
    async clearCart() {
      const userStore = useUserStore()
      
      if (userStore.isLoggedIn) {
        // 用户已登录，删除所有商品
        const allItems = [...this.items]
        for (const item of allItems) {
          await this.removeFromCart(item.id)
        }
      } else {
        // 用户未登录，清空本地存储
        this.items = []
        this.saveToLocalStorage()
      }
    },
    
    toggleSelectAll(selected) {
      this.items.forEach(item => {
        item.selected = selected
      })
      this.saveToLocalStorage()
    },
    
    async fetchCartFromServer() {
      try {
        const userStore = useUserStore()
        
        if (!userStore.isLoggedIn) return
        
        try {
          const response = await fetch('/api/cart/', {
            headers: {
              'Authorization': `Bearer ${userStore.token}`
            }
          })
          
          if (response.ok) {
            const data = await response.json()
            // 转换后端数据格式为前端格式
            this.items = Array.isArray(data.items) ? data.items.map(item => ({
              id: item.id,
              product_id: item.product ? item.product.id : null,
              name: item.product ? item.product.name : '未知商品',
              price: item.product ? parseFloat(item.product.price) : 0,
              quantity: item.quantity || 0,
              image_url: item.product ? `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(item.product.name)}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd` : '',
              selected: true
            })) : []
            this.saveToLocalStorage()
          } else if (response.status === 401 || response.status === 403) {
            // Token无效或过期，清除本地存储并提示用户重新登录
            userStore.logout()
            console.error('登录已过期，请重新登录')
          }
        } catch (apiError) {
          console.error('获取购物车数据失败:', apiError)
        }
      } catch (error) {
        console.error('获取购物车数据异常:', error)
      }
    },
    
    saveToLocalStorage() {
      try {
        // 检查localStorage是否可用
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('cart', JSON.stringify(this.items))
        }
      } catch (error) {
        console.error('保存购物车到本地存储失败:', error)
      }
    },
    
    loadFromLocalStorage() {
      try {
        // 检查localStorage是否可用
        if (typeof localStorage !== 'undefined') {
          const savedCart = localStorage.getItem('cart')
          if (savedCart) {
            try {
              const parsedCart = JSON.parse(savedCart)
              // 验证解析后的数据格式
              if (Array.isArray(parsedCart)) {
                this.items = parsedCart
              } else {
                console.error('购物车数据格式错误')
                this.items = []
              }
            } catch (parseError) {
              console.error('解析购物车数据失败:', parseError)
              this.items = []
            }
          }
        }
      } catch (error) {
        console.error('从本地存储加载购物车失败:', error)
        this.items = []
      }
    }
  }
})
