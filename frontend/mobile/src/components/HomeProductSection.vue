<template>
  <section class="home-products">
    <div class="section-header">
      <span>商品列表</span>
      <RouterLink to="/products">全部商品</RouterLink>
    </div>

    <section class="category-strip">
      <button class="category-pill" :class="{ active: !activeCategoryId }" @click="selectCategory(null)">全部</button>
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

    <div v-if="loading" class="loading-bar">加载中...</div>
    <section v-if="!loading && products.length === 0" class="state-card">暂无商品</section>

    <section v-else class="home-product-grid">
      <article v-for="item in products" :key="item.id" class="home-product-card">
        <div class="home-product-image">{{ item.main_image || item.name.slice(0, 2) }}</div>
        <div class="home-product-name">{{ item.name }}</div>
        <div class="home-product-price">￥{{ item.price }}</div>
        <div class="home-product-stock" :class="stockClass(item.stock_quantity)">
          {{ stockText(item.stock_quantity) }}
        </div>
        <button class="add-button" :disabled="item.stock_quantity <= 0" @click="handleAddToCart(item.id, $event)">
          {{ item.stock_quantity <= 0 ? "已售罄" : "加入购物车" }}
        </button>
      </article>
    </section>

    <div ref="loadMoreTrigger" class="load-more-trigger" />
    <div v-if="loadingMore" class="loading-bar">正在加载更多...</div>
    <div v-else-if="!hasMore && products.length > 0" class="end-text">没有更多商品了</div>

    <div
      v-if="feedbackMessage"
      class="feedback-bubble"
      :class="feedbackType"
      :style="{ left: `${feedbackX}px`, top: `${feedbackY}px` }"
    >
      {{ feedbackMessage }}
    </div>
  </section>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { fetchCategories, type Category } from "../api/home";
import { fetchProducts, type Product } from "../api/products";
import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../stores/cart";

const PAGE_SIZE = 6;

const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const loading = ref(false);
const loadingMore = ref(false);
const hasMore = ref(true);
const page = ref(1);
const categories = ref<Category[]>([]);
const products = ref<Product[]>([]);
const activeCategoryId = ref<number | null>(null);
const loadMoreTrigger = ref<HTMLElement | null>(null);
const feedbackMessage = ref("");
const feedbackType = ref<"success" | "error">("success");
const feedbackX = ref(0);
const feedbackY = ref(0);

let observer: IntersectionObserver | null = null;
let feedbackTimer: ReturnType<typeof setTimeout> | null = null;
type FeedbackAnchor = { x: number; y: number };

onMounted(async () => {
  categories.value = await fetchCategories();
  await reloadProducts();
  setupObserver();
});

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect();
    observer = null;
  }
  if (feedbackTimer) {
    clearTimeout(feedbackTimer);
    feedbackTimer = null;
  }
});

function setupObserver() {
  if (!loadMoreTrigger.value) {
    return;
  }
  observer = new IntersectionObserver((entries) => {
    const [entry] = entries;
    if (entry?.isIntersecting) {
      loadMore();
    }
  });
  observer.observe(loadMoreTrigger.value);
}

async function reloadProducts() {
  loading.value = true;
  page.value = 1;
  hasMore.value = true;
  try {
    const payload = await fetchProducts({
      categoryId: activeCategoryId.value,
      page: page.value,
      size: PAGE_SIZE,
    });
    products.value = payload;
    hasMore.value = payload.length === PAGE_SIZE;
    page.value = 2;
  } finally {
    loading.value = false;
  }
}

async function loadMore() {
  if (loading.value || loadingMore.value || !hasMore.value) {
    return;
  }
  loadingMore.value = true;
  try {
    const payload = await fetchProducts({
      categoryId: activeCategoryId.value,
      page: page.value,
      size: PAGE_SIZE,
    });
    if (payload.length === 0) {
      hasMore.value = false;
      return;
    }
    products.value = [...products.value, ...payload];
    hasMore.value = payload.length === PAGE_SIZE;
    page.value += 1;
  } finally {
    loadingMore.value = false;
  }
}

async function selectCategory(categoryId: number | null) {
  activeCategoryId.value = categoryId;
  await reloadProducts();
}

async function handleAddToCart(productId: number, event: MouseEvent) {
  const anchor = resolveFeedbackAnchor(event);
  if (!authStore.isAuthenticated) {
    showFeedback("请先登录", "error", anchor);
    await router.push("/login");
    return;
  }
  try {
    await cartStore.addItem(productId, 1);
    showFeedback("已加入购物车", "success", anchor);
  } catch {
    showFeedback("加入购物车失败", "error", anchor);
  }
}

function resolveFeedbackAnchor(event?: MouseEvent): FeedbackAnchor {
  if (event?.currentTarget instanceof HTMLElement) {
    const rect = event.currentTarget.getBoundingClientRect();
    return {
      x: rect.left + rect.width / 2,
      y: Math.max(rect.top - 12, 64),
    };
  }
  return { x: window.innerWidth / 2, y: Math.max(window.innerHeight * 0.72, 120) };
}

function showFeedback(message: string, type: "success" | "error", anchor?: FeedbackAnchor) {
  feedbackMessage.value = message;
  feedbackType.value = type;
  const target = anchor ?? resolveFeedbackAnchor();
  feedbackX.value = target.x;
  feedbackY.value = target.y;

  if (feedbackTimer) {
    clearTimeout(feedbackTimer);
  }
  feedbackTimer = setTimeout(() => {
    feedbackMessage.value = "";
    feedbackTimer = null;
  }, 1200);
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
.home-products {
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

.section-header a {
  color: #2563eb;
  text-decoration: none;
  font-size: 14px;
}

.category-strip {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
  overflow-x: auto;
}

.category-pill {
  min-width: 64px;
  min-height: 36px;
  border: none;
  border-radius: 999px;
  background: #e5e7eb;
  color: #4b5563;
  font-weight: 600;
}

.category-pill.active {
  background: #2563eb;
  color: #fff;
}

.loading-bar {
  margin: 10px 0;
  min-height: 36px;
  border-radius: 10px;
  background: linear-gradient(90deg, #dbeafe, #eff6ff);
  color: #1d4ed8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

.state-card {
  padding: 12px;
  border-radius: 14px;
  background: #f8fafc;
}

.home-product-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.home-product-card {
  padding: 12px;
  border-radius: 14px;
  background: #f8fafc;
}

.home-product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 96px;
  border-radius: 10px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 600;
}

.home-product-name {
  margin-top: 10px;
  color: #111827;
  font-size: 14px;
}

.home-product-price {
  margin-top: 6px;
  color: #dc2626;
  font-weight: 700;
}

.home-product-stock {
  margin-top: 6px;
  font-size: 13px;
}

.home-product-stock.normal {
  color: #059669;
}

.home-product-stock.low {
  color: #d97706;
}

.home-product-stock.soldout {
  color: #6b7280;
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

.add-button:disabled {
  background: #d1d5db;
  color: #6b7280;
}

.load-more-trigger {
  height: 1px;
}

.end-text {
  margin-top: 10px;
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
}

.feedback-bubble {
  position: fixed;
  transform: translate(-50%, -100%);
  padding: 6px 10px;
  border-radius: 999px;
  color: #fff;
  font-size: 12px;
  z-index: 40;
  pointer-events: none;
  animation: bubble-up 1.2s ease forwards;
}

.feedback-bubble.success {
  background: rgba(15, 23, 42, 0.88);
}

.feedback-bubble.error {
  background: rgba(220, 38, 38, 0.92);
}

@keyframes bubble-up {
  0% {
    opacity: 0;
    transform: translate(-50%, -90%);
  }
  20% {
    opacity: 1;
    transform: translate(-50%, -100%);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -125%);
  }
}
</style>
