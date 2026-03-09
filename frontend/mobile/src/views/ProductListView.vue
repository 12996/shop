<template>
  <div class="page-shell">
    <main class="page">
      <header class="topbar">
        <div>
          <div class="brand">无人超市</div>
          <h1 class="page-title">商品列表</h1>
        </div>
        <RouterLink class="cart-entry" to="/cart">购物车</RouterLink>
      </header>

      <section class="search-box">
        <input v-model.trim="keyword" type="text" placeholder="搜索商品名称" @keyup.enter="loadProducts" />
      </section>

      <section class="category-strip">
        <button class="category-pill" :class="{ active: !activeCategoryId }" @click="selectCategory(null)">
          全部
        </button>
        <button
          v-for="category in categories"
          :key="category.id"
          class="category-pill"
          :class="{ active: activeCategoryId === category.id }"
          @click="selectCategory(category.id)"
        >
          {{ category.name }}
        </button>
      </section>

      <section v-if="loading" class="state-card">加载中...</section>
      <section v-else-if="products.length === 0" class="state-card">未找到相关商品</section>

      <section v-else class="product-list">
        <article v-for="item in products" :key="item.id" class="product-card">
          <div class="image">{{ item.main_image || item.name.slice(0, 2) }}</div>
          <div class="name">{{ item.name }}</div>
          <div class="price">￥{{ item.price }}</div>
          <div class="stock" :class="stockClass(item.stock_quantity)">
            {{ stockText(item.stock_quantity) }}
          </div>
          <button class="action" :disabled="item.stock_quantity <= 0" @click="handleAddToCart(item.id)">
            {{ item.stock_quantity <= 0 ? "已售罄" : "加入购物车" }}
          </button>
        </article>
      </section>
    </main>

    <MobileTabBar />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";

import { fetchCategories, type Category } from "../api/home";
import { fetchProducts, type Product } from "../api/products";
import MobileTabBar from "../components/MobileTabBar.vue";
import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../stores/cart";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const loading = ref(false);
const keyword = ref(typeof route.query.keyword === "string" ? route.query.keyword : "");
const activeCategoryId = ref<number | null>(
  typeof route.query.categoryId === "string" ? Number(route.query.categoryId) : null,
);
const categories = ref<Category[]>([]);
const products = ref<Product[]>([]);

onMounted(async () => {
  categories.value = await fetchCategories();
  await loadProducts();
});

async function loadProducts() {
  loading.value = true;
  try {
    products.value = await fetchProducts({
      categoryId: activeCategoryId.value,
      keyword: keyword.value,
    });
  } finally {
    loading.value = false;
  }
}

async function selectCategory(categoryId: number | null) {
  activeCategoryId.value = categoryId;
  await router.replace({
    path: "/products",
    query: {
      ...(categoryId ? { categoryId: String(categoryId) } : {}),
      ...(keyword.value ? { keyword: keyword.value } : {}),
    },
  });
  await loadProducts();
}

async function handleAddToCart(productId: number) {
  if (!authStore.isAuthenticated) {
    await router.push("/login");
    return;
  }

  await cartStore.addItem(productId, 1);
}

function stockText(stockQuantity: number) {
  if (stockQuantity <= 0) {
    return "已售罄";
  }
  if (stockQuantity <= 5) {
    return `剩余 ${stockQuantity} 件`;
  }
  return "库存充足";
}

function stockClass(stockQuantity: number) {
  if (stockQuantity <= 0) {
    return "soldout";
  }
  if (stockQuantity <= 5) {
    return "low";
  }
  return "normal";
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

.cart-entry {
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

.category-strip {
  display: flex;
  gap: 8px;
  margin: 16px 0;
  overflow-x: auto;
}

.category-pill {
  min-width: 64px;
  min-height: 36px;
  border: none;
  border-radius: 999px;
  background: #e5e7eb;
  color: #4b5563;
}

.category-pill.active {
  background: #2563eb;
  color: #fff;
}

.state-card {
  padding: 20px;
  border-radius: 16px;
  background: #fff;
  color: #6b7280;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.product-card {
  padding: 12px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.image {
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

.name {
  margin-top: 10px;
  color: #111827;
  font-size: 14px;
}

.price {
  margin-top: 6px;
  color: #dc2626;
  font-weight: 700;
}

.stock {
  margin-top: 6px;
  font-size: 13px;
}

.stock.normal {
  color: #059669;
}

.stock.low {
  color: #d97706;
}

.stock.soldout {
  color: #6b7280;
}

.action {
  width: 100%;
  min-height: 38px;
  margin-top: 10px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
}

.action:disabled {
  background: #d1d5db;
  color: #6b7280;
}
</style>
