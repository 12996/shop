<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>用户首页</h2>
        <p>公告、分类入口和推荐商品会直接从后端加载。</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="search-card">
      <input v-model.trim="keyword" type="text" placeholder="搜索商品名称" @keyup.enter="goToProducts()" />
      <button class="primary-button" @click="goToProducts()">搜索</button>
    </section>

    <section class="content-card">
      <h3>公告</h3>
      <p>{{ announcement?.content || "暂无公告" }}</p>
    </section>

    <section class="content-card">
      <h3>分类入口</h3>
      <div class="category-list">
        <button v-for="category in categories" :key="category.id" class="chip" @click="goToProducts(category.id)">
          {{ category.name }}
        </button>
      </div>
    </section>

    <section class="content-card">
      <div class="section-title">
        <h3>推荐商品</h3>
        <RouterLink class="link-button" to="/user/products">查看全部</RouterLink>
      </div>

      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="recommendations.length === 0" class="state-text">暂无推荐商品</div>
      <div v-else class="product-grid">
        <article v-for="item in recommendations" :key="item.id" class="product-card">
          <div class="image-box">{{ item.product_image || item.product_name.slice(0, 2) }}</div>
          <div class="product-name">{{ item.product_name }}</div>
          <div class="product-price">￥{{ item.product_price }}</div>
          <button class="primary-button" @click="addToCart(item.product)">加入购物车</button>
        </article>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { addCartItem } from "../../api/cart";
import { fetchHomeData, type HomeAnnouncement, type HomeRecommendation } from "../../api/home";
import { fetchCategories, type Category } from "../../api/products";

const router = useRouter();

const loading = ref(false);
const keyword = ref("");
const errorMessage = ref("");
const announcement = ref<HomeAnnouncement | null>(null);
const categories = ref<Category[]>([]);
const recommendations = ref<HomeRecommendation[]>([]);

onMounted(async () => {
  await loadData();
});

async function loadData() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const [homeData, categoryData] = await Promise.all([fetchHomeData(), fetchCategories()]);
    announcement.value = homeData.announcement;
    recommendations.value = homeData.recommendations;
    categories.value = categoryData;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

function goToProducts(categoryId?: number) {
  router.push({
    path: "/user/products",
    query: {
      ...(categoryId ? { categoryId: String(categoryId) } : {}),
      ...(keyword.value ? { keyword: keyword.value } : {}),
    },
  });
}

async function addToCart(productId: number) {
  try {
    await addCartItem({ product_id: productId, quantity: 1 });
    await router.push("/user/cart");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加入购物车失败";
  }
}
</script>

<style scoped>
.page-card,
.content-card,
.search-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.content-card,
.search-card {
  margin-top: 20px;
}

.page-header h2,
.content-card h3 {
  margin: 0;
}

.page-header p,
.content-card p,
.state-text {
  margin: 8px 0 0;
  color: #6b7280;
}

.search-card {
  display: flex;
  gap: 12px;
}

.search-card input {
  flex: 1;
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
}

.category-list,
.product-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}

.chip,
.primary-button {
  min-height: 38px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
}

.chip {
  background: #eff6ff;
  color: #1d4ed8;
}

.primary-button {
  background: #2563eb;
  color: #fff;
}

.product-card {
  width: 200px;
  padding: 16px;
  border-radius: 16px;
  background: #f8fafc;
}

.image-box {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 96px;
  border-radius: 12px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 600;
}

.product-name,
.product-price {
  margin-top: 10px;
}

.product-price {
  color: #dc2626;
  font-weight: 700;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.link-button {
  color: #2563eb;
  text-decoration: none;
}

.error-text {
  margin-top: 16px;
  color: #dc2626;
}
</style>
