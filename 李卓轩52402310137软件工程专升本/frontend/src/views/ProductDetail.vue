<template>
  <div class="product-detail">
    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-3">正在加载商品详情...</p>
    </div>

    <!-- 商品内容 -->
    <div v-else>
      <!-- 面包屑导航 -->
      <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <router-link to="/">首页</router-link>
          </li>
          <li class="breadcrumb-item">
            <router-link :to="`/category/${product.category_id || 1}`">
              {{ categoryName }}
            </router-link>
          </li>
          <li class="breadcrumb-item active" aria-current="page">
            {{ product.name || '商品详情' }}
          </li>
        </ol>
      </nav>

      <!-- 商品信息 -->
      <div class="row mb-6">
        <!-- 商品图片 -->
        <div class="col-lg-5">
          <div class="product-images">
            <div class="main-image mb-3">
              <img :src="product.image_url" :alt="product.name || '商品图片'" class="img-fluid rounded">
            </div>
            <div class="thumbnail-images d-flex">
              <div v-for="(img, index) in (product.images || [])" :key="index" class="thumbnail-item me-2">
                <img :src="img" :alt="`商品图片 - ${index + 1}`" class="img-fluid rounded" style="width: 80px; height: 80px; object-fit: cover;">
              </div>
            </div>
          </div>
        </div>

        <!-- 商品详情 -->
        <div class="col-lg-7">
          <div class="product-info">
            <h1 class="product-name mb-2">{{ product.name }}</h1>
            <div class="product-rating mb-3">
              <div class="stars">
                <i v-for="i in 5" :key="i" class="bi" :class="i <= (product.rating || 5) ? 'bi-star-fill text-warning' : 'bi-star text-muted'">
                </i>
              </div>
              <span class="rating-text">({{ product.review_count || 0 }} 评价)</span>
            </div>
            <div class="product-price mb-4">
              <span class="price-label">价格:</span>
              <span class="price-value">¥{{ (product.price || 0).toFixed(2) }}</span>
              <span v-if="product.original_price" class="original-price">
                ¥{{ product.original_price.toFixed(2) }}
              </span>
            </div>
            <div class="product-sales mb-4">
              <span>已售 {{ product.sold_count || 0 }} | 库存 {{ product.stock || 100 }}</span>
            </div>
            <div class="product-description mb-4">
              <p>{{ product.description || '暂无描述' }}</p>
            </div>

            <!-- 购买选项 -->
            <div class="purchase-options mb-6">
              <div class="quantity-control mb-4">
                <label for="quantity" class="me-3">数量:</label>
                <div class="input-group" style="width: 120px;">
                  <button @click="decreaseQuantity" class="btn btn-outline-secondary" type="button">-
                  </button>
                  <input v-model.number="quantity" type="number" class="form-control text-center" id="quantity" min="1" :max="product.stock || 100">
                  <button @click="increaseQuantity" class="btn btn-outline-secondary" type="button">+
                  </button>
                </div>
              </div>

              <!-- 购买按钮 -->
              <div class="action-buttons">
                <button @click="addToCart" class="btn btn-primary btn-lg me-3">
                  <i class="bi bi-cart-plus me-2"></i>加入购物车
                </button>
                <button @click="buyNow" class="btn btn-danger btn-lg">
                  <i class="bi bi-bag-check me-2"></i>立即购买
                </button>
              </div>
            </div>

            <!-- 商品属性 -->
            <div class="product-attributes">
              <div class="attribute-item mb-2">
                <span class="attribute-label">品牌:</span>
                <span class="attribute-value">{{ product.brand || '-' }}</span>
              </div>
              <div class="attribute-item mb-2">
                <span class="attribute-label">产地:</span>
                <span class="attribute-value">{{ product.origin || '-' }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">重量:</span>
                <span class="attribute-value">{{ product.weight || 0 }}g</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 商品详情标签页 -->
      <div class="product-tabs mb-6">
        <ul class="nav nav-tabs" id="productTab" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active" id="detail-tab" data-bs-toggle="tab" data-bs-target="#detail" type="button" role="tab" aria-controls="detail" aria-selected="true">
              商品详情
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="reviews-tab" data-bs-toggle="tab" data-bs-target="#reviews" type="button" role="tab" aria-controls="reviews" aria-selected="false">
              用户评价 ({{ product.review_count || 0 }})
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="specs-tab" data-bs-toggle="tab" data-bs-target="#specs" type="button" role="tab" aria-controls="specs" aria-selected="false">
              规格参数
            </button>
          </li>
        </ul>
        <div class="tab-content" id="productTabContent">
          <!-- 商品详情 -->
          <div class="tab-pane fade show active" id="detail" role="tabpanel" aria-labelledby="detail-tab">
            <div class="p-4 bg-white rounded">
              <div v-html="product.detail || '<p>暂无详细描述</p>'"></div>
            </div>
          </div>

          <!-- 用户评价 -->
          <div class="tab-pane fade" id="reviews" role="tabpanel" aria-labelledby="reviews-tab">
            <div class="p-4 bg-white rounded">
              <div v-for="review in reviews" :key="review.id" class="review-item mb-4 pb-4 border-bottom">
                <div class="review-header d-flex justify-content-between mb-2">
                  <div class="reviewer-info">
                    <span class="reviewer-name">{{ review.username }}</span>
                    <span class="review-date">{{ review.created_at }}</span>
                  </div>
                  <div class="review-rating">
                    <i v-for="i in 5" :key="i" class="bi" :class="i <= review.rating ? 'bi-star-fill text-warning' : 'bi-star text-muted'">
                    </i>
                  </div>
                </div>
                <div class="review-content">
                  <p>{{ review.content }}</p>
                </div>
                <div class="review-images d-flex mt-2">
                  <img v-for="(img, index) in (review.images || [])" :key="index" :src="img" :alt="`评价图片 ${index + 1}`" class="img-fluid me-2" style="width: 100px; height: 100px; object-fit: cover;">
                </div>
              </div>
              <div v-if="reviews.length === 0" class="no-reviews text-center py-4">
                <p>暂无评价</p>
              </div>
            </div>
          </div>

          <!-- 规格参数 -->
          <div class="tab-pane fade" id="specs" role="tabpanel" aria-labelledby="specs-tab">
            <div class="p-4 bg-white rounded">
              <table class="table table-bordered">
                <tbody>
                  <tr>
                    <th>商品名称</th>
                    <td>{{ product.name || '-' }}</td>
                  </tr>
                  <tr>
                    <th>商品编号</th>
                    <td>{{ product.sku || '-' }}</td>
                  </tr>
                  <tr>
                    <th>品牌</th>
                    <td>{{ product.brand || '-' }}</td>
                  </tr>
                  <tr>
                    <th>产地</th>
                    <td>{{ product.origin || '-' }}</td>
                  </tr>
                  <tr>
                    <th>重量</th>
                    <td>{{ product.weight || 0 }}g</td>
                  </tr>
                  <tr>
                    <th>材质</th>
                    <td>{{ product.material || '-' }}</td>
                  </tr>
                  <tr>
                    <th>尺寸</th>
                    <td>{{ product.size || '-' }}</td>
                  </tr>
                  <tr>
                    <th>颜色</th>
                    <td>{{ product.color || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- 相关商品 -->
      <div class="related-products">
        <h3 class="mb-4">相关商品</h3>
        <div class="row">
          <div v-for="relatedProduct in relatedProducts" :key="relatedProduct.id" class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="product-card card h-100">
              <router-link :to="`/product/${relatedProduct.id}`" class="text-decoration-none">
                <img :src="relatedProduct.image_url" :alt="relatedProduct.name" class="card-img-top">
                <div class="card-body">
                  <h5 class="card-title text-truncate">{{ relatedProduct.name }}</h5>
                  <div class="price">¥{{ (relatedProduct.price || 0).toFixed(2) }}</div>
                  <div class="sold-count">已售 {{ relatedProduct.sold_count || 0 }}</div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'

export default {
  name: 'ProductDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const cartStore = useCartStore()
    const productId = ref(route.params.id)
    const product = ref({})
    const categoryName = ref('')
    const reviews = ref([])
    const relatedProducts = ref([])
    const quantity = ref(1)
    const loading = ref(true)

    // 获取商品详情
    const fetchProductDetail = async () => {
      loading.value = true
      try {
        const response = await fetch(`/api/products/products/${productId.value}/`)
        if (response.ok) {
          product.value = await response.json()
          product.value.price = parseFloat(product.value.price)
          product.value.image_url = `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(product.value.name)}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd`
          // 获取分类名称
          fetchCategoryName(product.value.category_id)
        } else {
          throw new Error('API返回错误')
        }
      } catch (error) {
        console.error('获取商品详情失败，使用模拟数据:', error)
        const mockProducts = [
          { id: 1, name: '苹果 iPhone 15 Pro Max 256GB', price: 9999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20smartphone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1234, stock: 100, description: 'Apple最新款iPhone，搭载A17 Pro芯片，钛金属设计，专业摄影系统', brand: 'Apple', origin: '中国', weight: 221, material: '钛金属', size: '160.8×77.6×8.25mm', color: '深空黑', sku: 'IPHONE15PM256', rating: 4.8, review_count: 345, category_id: 1, images: [], detail: '<p>详细描述...</p>' },
          { id: 2, name: '华为 Mate 60 Pro 5G手机', price: 6999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20mobile%20phone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 856, stock: 80, description: '华为旗舰手机，麒麟9000S芯片，卫星通信，超可靠玄武架构', brand: '华为', origin: '中国', weight: 225, material: '陶瓷后盖', size: '161.4×76.1×8.1mm', color: '雅丹黑', sku: 'MATE60PRO', rating: 4.7, review_count: 234, category_id: 1, images: [], detail: '<p>详细描述...</p>' },
          { id: 3, name: '索尼 WH-1000XM5 无线降噪耳机', price: 2499.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20headphones%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 2341, stock: 150, description: '索尼旗舰降噪耳机，全新设计，业界领先的降噪性能，30小时续航', brand: '索尼', origin: '日本', weight: 250, material: '工程塑料', size: '可折叠', color: '黑色', sku: 'WH1000XM5', rating: 4.9, review_count: 456, category_id: 2, images: [], detail: '<p>详细描述...</p>' },
          { id: 4, name: 'MacBook Pro 14英寸 M3芯片', price: 12999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20laptop%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 567, stock: 60, description: 'Apple M3芯片，Liquid Retina XDR显示屏，18小时续航', brand: 'Apple', origin: '中国', weight: 1610, material: '铝合金', size: '31.26×22.12×1.55cm', color: '深空灰', sku: 'MBP14M3', rating: 4.9, review_count: 189, category_id: 3, images: [], detail: '<p>详细描述...</p>' },
          { id: 5, name: '戴森 V15 Detect 无线吸尘器', price: 4990.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20vacuum%20cleaner%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 789, stock: 90, description: '激光探测灰尘，可视化除尘，60分钟续航', brand: '戴森', origin: '英国', weight: 2610, material: 'ABS塑料', size: '126.6×25.6×25cm', color: '紫镍色', sku: 'V15DETECT', rating: 4.6, review_count: 267, category_id: 4, images: [], detail: '<p>详细描述...</p>' },
          { id: 6, name: '任天堂 Switch OLED 游戏机', price: 2199.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20game%20console%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1876, stock: 120, description: '7英寸OLED屏幕，随时随地畅玩，Switch家族新成员', brand: '任天堂', origin: '日本', weight: 420, material: '工程塑料', size: '24.2×10.2×13.9cm', color: '白色', sku: 'SWITCHOLED', rating: 4.8, review_count: 534, category_id: 5, images: [], detail: '<p>详细描述...</p>' },
          { id: 7, name: 'SK-II 神仙水护肤精华 230ml', price: 1590.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20skincare%20cosmetics%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 3456, stock: 200, description: '经典护肤精华，90%以上PITERA™精华，改善肤质', brand: 'SK-II', origin: '日本', weight: 300, material: '玻璃瓶装', size: '230ml', color: '透明', sku: 'SKII230', rating: 4.7, review_count: 789, category_id: 6, images: [], detail: '<p>详细描述...</p>' },
          { id: 8, name: 'iPad Pro 12.9英寸 M2芯片', price: 8999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20tablet%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 432, stock: 75, description: 'M2芯片，Liquid Retina XDR显示屏，专业级性能', brand: 'Apple', origin: '中国', weight: 682, material: '铝合金', size: '280.6×214.9×6.4mm', color: '深空灰', sku: 'IPADPRO129', rating: 4.8, review_count: 156, category_id: 3, images: [], detail: '<p>详细描述...</p>' },
          { id: 9, name: '小米空气净化器 4 Pro', price: 1499.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20air%20purifier%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 987, stock: 110, description: 'CADR值500m³/h，OLED触控屏，智能控制', brand: '小米', origin: '中国', weight: 7800, material: 'ABS塑料', size: '260×260×520mm', color: '白色', sku: 'MIAP4PRO', rating: 4.5, review_count: 312, category_id: 4, images: [], detail: '<p>详细描述...</p>' },
          { id: 10, name: '佳能 EOS R6 Mark II 全画幅相机', price: 16999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20camera%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 234, stock: 45, description: '2420万像素全画幅CMOS，40fps连拍，8K视频', brand: '佳能', origin: '日本', weight: 680, material: '镁合金', size: '138.4×98.4×88.4mm', color: '黑色', sku: 'EOSR6M2', rating: 4.9, review_count: 89, category_id: 2, images: [], detail: '<p>详细描述...</p>' },
          { id: 11, name: '优衣库 男士羽绒服 轻薄款', price: 399.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20jacket%20clothing%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 5678, stock: 300, description: '轻薄保暖，90%白鸭绒，便携收纳', brand: '优衣库', origin: '中国', weight: 350, material: '尼龙', size: 'S-XXL', color: '黑色', sku: 'UNIQLODJ', rating: 4.6, review_count: 987, category_id: 7, images: [], detail: '<p>详细描述...</p>' },
          { id: 12, name: '三只松鼠 坚果大礼包 1kg', price: 99.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20nuts%20snacks%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 8901, stock: 500, description: '多种坚果组合，新鲜美味，送礼自用两相宜', brand: '三只松鼠', origin: '中国', weight: 1000, material: '纸质包装', size: '1kg', color: '彩色', sku: 'SSNUT1KG', rating: 4.7, review_count: 1567, category_id: 8, images: [], detail: '<p>详细描述...</p>' },
          { id: 13, name: 'Kindle Paperwhite 电子书阅读器', price: 999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20ebook%20reader%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1234, stock: 130, description: '6.8英寸显示屏，可调节冷暖色温，防水设计', brand: 'Amazon', origin: '中国', weight: 205, material: '工程塑料', size: '174×125×8.1mm', color: '黑色', sku: 'KPW5', rating: 4.8, review_count: 423, category_id: 9, images: [], detail: '<p>详细描述...</p>' },
          { id: 14, name: 'Beats Studio Buds+ 真无线耳机', price: 1099.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20earbuds%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 2345, stock: 160, description: '主动降噪，苹果H1芯片，36小时续航', brand: 'Beats', origin: '中国', weight: 51, material: '塑料', size: '入耳式', color: '黑色', sku: 'BSBUDS', rating: 4.5, review_count: 654, category_id: 2, images: [], detail: '<p>详细描述...</p>' },
          { id: 15, name: '兰蔻小黑瓶精华肌底液 100ml', price: 1080.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20serum%20cosmetics%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 4567, stock: 180, description: '修护肌肤，强韧屏障，焕亮肤色', brand: '兰蔻', origin: '法国', weight: 150, material: '玻璃瓶装', size: '100ml', color: '黑色', sku: 'LANCOME100', rating: 4.6, review_count: 876, category_id: 6, images: [], detail: '<p>详细描述...</p>' },
          { id: 16, name: '乐高 哈利波特 霍格沃茨城堡', price: 3999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20lego%20toy%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 678, stock: 35, description: '6020片积木，还原经典场景，收藏级模型', brand: '乐高', origin: '丹麦', weight: 5500, material: 'ABS塑料', size: '58×48×37cm', color: '多色', sku: 'LEGO71043', rating: 4.9, review_count: 123, category_id: 10, images: [], detail: '<p>详细描述...</p>' }
        ]
        const mockProduct = mockProducts.find(p => p.id === parseInt(productId.value)) || mockProducts[0]
        product.value = mockProduct
        categoryName.value = '商品分类'
      } finally {
        loading.value = false
      }
    }

    // 获取分类名称
    const fetchCategoryName = async (categoryId) => {
      try {
        const response = await fetch(`/api/products/categories/${categoryId}/`)
        if (response.ok) {
          const categoryData = await response.json()
          categoryName.value = categoryData.name
        }
      } catch (error) {
        console.error('获取分类名称失败:', error)
      }
    }

    // 获取用户评价
    const fetchReviews = async () => {
      try {
        const response = await fetch(`/api/products/${productId.value}/reviews/`)
        if (response.ok) {
          reviews.value = await response.json()
        } else {
          throw new Error('API返回错误')
        }
      } catch (error) {
        console.error('获取用户评价失败，使用模拟数据:', error)
        reviews.value = [
          { id: 1, username: '张**', created_at: '2024-01-15', rating: 5, content: '非常好的商品，质量很好，物流也很快！', images: [] },
          { id: 2, username: '李**', created_at: '2024-01-10', rating: 4, content: '商品不错，性价比很高，推荐购买。', images: [] },
          { id: 3, username: '王**', created_at: '2024-01-05', rating: 5, content: '买了很多次了，一如既往的好！', images: [] }
        ]
      }
    }

    // 获取相关商品
    const fetchRelatedProducts = async () => {
      try {
        const response = await fetch(`/api/products/${productId.value}/related/`)
        if (response.ok) {
          relatedProducts.value = await response.json()
          relatedProducts.value.forEach((product) => {
            product.image_url = `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20${encodeURIComponent(product.name)}%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd`
          })
        } else {
          throw new Error('API返回错误')
        }
      } catch (error) {
        console.error('获取相关商品失败，使用模拟数据:', error)
        const mockProducts = [
          { id: 1, name: '苹果 iPhone 15 Pro Max 256GB', price: 9999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20smartphone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 1234 },
          { id: 2, name: '华为 Mate 60 Pro 5G手机', price: 6999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20mobile%20phone%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 856 },
          { id: 3, name: '索尼 WH-1000XM5 无线降噪耳机', price: 2499.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20headphones%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 2341 },
          { id: 4, name: 'MacBook Pro 14英寸 M3芯片', price: 12999.00, image_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20laptop%20e-commerce%20product%20image%2C%20high%20quality&image_size=square_hd', sold_count: 567 }
        ]
        relatedProducts.value = mockProducts
      }
    }

    // 增加数量
    const increaseQuantity = () => {
      if (quantity.value < product.value.stock) {
        quantity.value++
      }
    }

    // 减少数量
    const decreaseQuantity = () => {
      if (quantity.value > 1) {
        quantity.value--
      }
    }

    // 添加到购物车
    const addToCart = async () => {
      try {
        // 验证商品数据
        if (!product.value || !product.value.id) {
          alert('商品信息无效')
          return
        }
        
        // 验证数量
        if (!quantity.value || quantity.value< 1) {
          alert('请选择有效的商品数量')
          return
        }
        
        await cartStore.addToCart(product.value, quantity.value)
        alert('商品已添加到购物车！')
      } catch (error) {
        console.error('添加商品失败:', error)
        if (error.message && error.message.includes('登录已过期')) {
          alert('登录已过期，请重新登录')
          router.push('/login')
        } else {
          alert(`添加商品失败: ${error.message || '请重试'}`)
        }
      }
    }

    // 立即购买
    const buyNow = async () => {
      try {
        // 添加到购物车
        await cartStore.addToCart(product.value, quantity.value)
        // 跳转到结算页面
        router.push('/checkout')
      } catch (error) {
        console.error('添加商品失败:', error)
        alert('添加商品失败，请重试')
      }
    }

    // 监听路由参数变化
    watch(() => route.params.id, (newId) => {
      productId.value = newId
      quantity.value = 1
      fetchProductDetail()
      fetchReviews()
      fetchRelatedProducts()
    })

    onMounted(() => {
      fetchProductDetail()
      fetchReviews()
      fetchRelatedProducts()
    })

    return {
      productId,
      product,
      categoryName,
      reviews,
      relatedProducts,
      quantity,
      loading,
      increaseQuantity,
      decreaseQuantity,
      addToCart,
      buyNow
    }
  }
}
</script>

<style scoped>
/* 商品信息样式 */
.product-name {
  font-size: 1.8rem;
  font-weight: bold;
}

.product-rating {
  display: flex;
  align-items: center;
}

.stars {
  margin-right: 10px;
}

.price-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #dc3545;
  margin-right: 15px;
}

.original-price {
  font-size: 1.2rem;
  color: #6c757d;
  text-decoration: line-through;
}

.product-sales {
  color: #6c757d;
}

.product-description {
  color: #333;
  line-height: 1.5;
}

.attribute-label {
  font-weight: bold;
  margin-right: 10px;
}

/* 标签页样式 */
.product-tabs {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-tabs {
  border-bottom: 1px solid #dee2e6;
}

.nav-tabs .nav-link {
  padding: 1rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
}

.tab-content {
  padding: 2rem;
}

/* 评价样式 */
.review-item {
  transition: all 0.3s ease;
}

.review-item:hover {
  background-color: #f8f9fa;
  padding-left: 10px;
  border-left: 3px solid #007bff;
}

/* 相关商品样式 */
.related-products {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
}

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

/* 响应式调整 */
@media (max-width: 768px) {
  .product-name {
    font-size: 1.4rem;
  }
  
  .price-value {
    font-size: 1.4rem;
  }
  
  .tab-content {
    padding: 1rem;
  }
}
</style>