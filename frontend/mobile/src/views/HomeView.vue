<template>
  <div class="page-shell">
    <main class="page">
      <header class="topbar">
        <div>
          <div class="brand">无人超市</div>
          <h1 class="page-title">首页</h1>
        </div>
        <RouterLink class="order-entry" to="/orders">我的订单</RouterLink>
      </header>

      <section class="search-box">
        <input v-model.trim="keyword" type="text" placeholder="搜索商品或分类" @keyup.enter="goToProducts()" />
      </section>

      <section class="notice-card">
        <div class="section-header">
          <span>公告</span>
        </div>
        <p v-if="announcement">{{ announcement.content }}</p>
        <p v-else>暂无公告</p>
      </section>

      <section class="category-section">
        <div class="section-header">
          <span>分类入口</span>
        </div>
        <div class="category-grid">
          <button
            v-for="category in categories"
            :key="category.id"
            class="category-chip"
            @click="goToProducts(category.id)"
          >
            {{ category.name }}
          </button>
        </div>
      </section>

      <section class="recommend-section">
        <div class="section-header">
          <span>推荐商品</span>
          <RouterLink to="/products">查看全部</RouterLink>
        </div>

        <div v-if="loading" class="state-card">加载中...</div>
        <div v-else-if="recommendations.length === 0" class="state-card">暂无推荐商品</div>

        <div v-else class="product-list">
          <article v-for="item in recommendations" :key="item.id" class="product-card">
            <div class="product-image">{{ item.product_image || item.product_name.slice(0, 2) }}</div>
            <div class="product-name">{{ item.product_name }}</div>
            <div class="product-price">￥{{ item.product_price }}</div>
            <button class="add-button" @click="handleAddToCart(item.product)">加入购物车</button>
          </article>
        </div>
      </section>
    </main>

    <MobileTabBar />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import {
  fetchCategories,
  fetchHomeData,
  type Announcement,
  type Category,
  type Recommendation,
} from "../api/home";
import MobileTabBar from "../components/MobileTabBar.vue";
import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../stores/cart";

const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const loading = ref(false);
const keyword = ref("");
const announcement = ref<Announcement | null>(null);
const categories = ref<Category[]>([]);
const recommendations = ref<Recommendation[]>([]);

onMounted(async () => {
  loading.value = true;
  try {
    const [homePayload, categoryPayload] = await Promise.all([fetchHomeData(), fetchCategories()]);
    announcement.value = homePayload.announcement;
    recommendations.value = homePayload.recommendations;
    categories.value = categoryPayload;
  } finally {
    loading.value = false;
  }
});

function goToProducts(categoryId?: number) {
  router.push({
    path: "/products",
    query: {
      ...(categoryId ? { categoryId: String(categoryId) } : {}),
      ...(keyword.value ? { keyword: keyword.value } : {}),
    },
  });
}

async function handleAddToCart(productId: number) {
  if (!authStore.isAuthenticated) {
    await router.push("/login");
    return;
  }

  await cartStore.addItem(productId, 1);
}
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  background: #f8fafc;
}

.page {
  padding: 20px 16px 88px;
  box-sizing: border-box;
  font-family: sans-serif;
}

.topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.brand {
  font-size: 13px;
  color: #2563eb;
  font-weight: 600;
}

.page-title {
  margin: 8px 0 0;
  font-size: 26px;
  color: #111827;
}

.order-entry,
.section-header a {
  color: #2563eb;
  text-decoration: none;
  font-size: 14px;
}

.search-box input {
  width: 100%;
  min-height: 44px;
  border: 1px solid #d1d5db;
  border-radius: 14px;
  padding: 0 14px;
  box-sizing: border-box;
}

.notice-card,
.category-section,
.recommend-section {
  margin-top: 16px;
  padding: 16px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  color: #111827;
  font-weight: 600;
}

.notice-card p {
  margin: 0;
  color: #4b5563;
  line-height: 1.5;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.category-chip {
  min-height: 40px;
  border: none;
  border-radius: 12px;
  background: #eff6ff;
  color: #1d4ed8;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.product-card,
.state-card {
  padding: 12px;
  border-radius: 14px;
  background: #f8fafc;
}

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 88px;
  border-radius: 12px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 600;
  text-align: center;
}

.product-name {
  margin-top: 10px;
  color: #111827;
  font-size: 14px;
}

.product-price {
  margin-top: 6px;
  color: #dc2626;
  font-weight: 600;
}

.add-button {
  width: 100%;
  min-height: 38px;
  margin-top: 10px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
}
</style>
